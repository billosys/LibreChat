import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
PLAN=Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
S=PLAN/'project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design'
P=S/'artifacts/cc-evidence02'
OUT=Path('/tmp/guildhall-cdc-review02')
records=[]
def run(argv,cwd=PLAN):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,text=True,capture_output=True)
 r=dict(argv=list(map(str,argv)),cwd=str(cwd),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr);records.append(r);return r
def hashes(p):return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.iterdir()) if f.is_file()}
def seal(p):
 (p/'SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in hashes(p).items() if k!='SHA256SUMS'))
before=hashes(P)
result={'reviewedCommit':'5d94ef8d8da18b636279553ed037b906259b2882','observedPlanningHead':run(['git','rev-parse','HEAD'])['stdout'].strip(),'packetBefore':before}
assert result['reviewedCommit']=='5d94ef8d8da18b636279553ed037b906259b2882'
for f in P.iterdir():
 if f.is_file():
  committed=subprocess.check_output(['git','show',result['reviewedCommit']+':'+str(f.relative_to(PLAN))],cwd=PLAN)
  assert hashlib.sha256(committed).hexdigest()==before[f.name],f
changed=run(['git','diff-tree','--no-commit-id','--name-only','-r',result['reviewedCommit']])['stdout'].splitlines()
assert set(changed)=={str(f.relative_to(PLAN)) for f in P.iterdir() if f.is_file()}
message=run(['git','show','-s','--format=%B',result['reviewedCommit']])['stdout']
for footer in ['Co-authored-by: Codex <noreply@openai.com>','Co-authored-by: Billo AI <ai-engineering@billo.systems>']:assert message.count(footer)==1
result['reviewedPacketMatchesCommit']=True
result['ccCommitScopeAndTrailersValid']=True
valid=run([sys.executable,P/'replay.py','--verify','--packet',P]);result['validVerifyExit']=valid['exitCode'];assert valid['exitCode']==0
result['validVerify']=json.loads(valid['stdout'])
with tempfile.TemporaryDirectory(prefix='cdc02-selftest-') as d:
 t=Path(d)/'packet';shutil.copytree(P,t)
 r=run([sys.executable,P/'replay.py','--self-test','--packet',t]);result['selfTestExit']=r['exitCode'];assert r['exitCode']==0
 result['selfTest']=json.loads(r['stdout']);result['selfTestCopyModified']=hashes(t)!=before
with tempfile.TemporaryDirectory(prefix='cdc02-corrupt-result-') as d:
 t=Path(d)/'packet';shutil.copytree(P,t)
 data=json.loads((t/'replay-result.json').read_text());assert data['success'] is True;data['success']=False
 (t/'replay-result.json').write_text(json.dumps(data,indent=2)+'\n');seal(t)
 r=run([sys.executable,P/'replay.py','--verify','--packet',t]);result['resealedWrongSubmittedSuccess']={'exitCode':r['exitCode'],'rejected':r['exitCode']!=0,'mutation':'submitted success true -> false; manifest recalculated'}
# Check actual production verification preflight, not a separate tuple expression.
spec=importlib.util.spec_from_file_location('cc02',P/'replay.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
env, cmds=m.collect_environment();env['sourceHead']='0'*40;m.collect_environment=lambda:(env,cmds)
calls=[]
def runner():calls.append(1);return {'exitCode':0},json.loads(m.SEALED_RESULT.read_text())
try:m.verify_packet(P,injected_runner=runner);pre={'rejected':False}
except m.EvidenceError as e:pre={'rejected':True,'error':str(e)}
pre['runnerCalls']=len(calls);result['productionPathWrongHead']=pre
matrix=json.loads(m.MATRIX.read_text())
result['ancillaryQuery']={'actualTopLevel':{k:matrix.get(k) for k in ['providerOnly','interfaceOnly','implicit']},'requiredPerRecord':[{k:r[k] for k in ['name','providerOnly','interfaceOnly','implicit']} for r in matrix['records']]}
# Freeze the historical manifest set to this reviewed commit.
manifest_paths=run(['git','ls-tree','-r','--name-only',result['reviewedCommit'],'--','project01-portable-persistence'])['stdout'].splitlines()
verified=[]
for rel in manifest_paths:
 if Path(rel).name!='SHA256SUMS':continue
 f=PLAN/rel
 for line in f.read_text().splitlines():
  if not line.strip():continue
  expected,name=line.split(None,1);p=f.parent/name.lstrip('*');actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==expected,(p,actual,expected);verified.append(str(p.relative_to(PLAN)))
result['historicalManifestEntriesVerified']=len(verified);result['historicalFiles']=verified
result['packetAfter']=hashes(P);assert result['packetAfter']==before
result['sourceStatus']=run(['git','status','--porcelain','--untracked-files=all'],m.SOURCE)['stdout'];assert result['sourceStatus']==''
result['planningStatus']=run(['git','status','--porcelain','--untracked-files=all'])['stdout']
result['actualSubmittedMatchesBaseline']=json.loads((P/'replay-result.json').read_text())==json.loads(m.SEALED_RESULT.read_text());assert result['actualSubmittedMatchesBaseline']
result['originalAncillaryQuery']=run(['jq','-c','{sourceHead,exclusions,providerOnly,interfaceOnly,implicit}',m.MATRIX])
result['emptyConversationQuery']=run(['jq','-c','[.records[]|select(.name=="conversationSchema")|.fields[]]',m.MATRIX])
result['correctFieldCounts']=run(['jq','-c','[.records[]|{name,fields:(.fields|length)}]',m.MATRIX])
result['correctAncillaryQuery']=run(['jq','-c','{sourceHead,exclusions,records:[.records[]|{name,providerOnly,interfaceOnly,implicit}]}',m.MATRIX])
result['ccCommit']=run(['git','show','--format=fuller','--stat',result['reviewedCommit']])
result['namedReadContract']=run(['cat',S/'artifacts/design-pass05/read-contract.md'])
result['publicProjection']=run(['sed','-n','456,481p','packages/data-schemas/src/methods/message.ts'],m.SOURCE)
for path,start,end in [('packages/data-provider/src/types/web.ts',19,58),('packages/data-provider/src/types/files.ts',150,221),('packages/data-provider/src/types/agents.ts',81,135),('packages/data-provider/src/schemas.ts',1039,1074),('packages/data-schemas/src/methods/conversation.ts',2060,2078)]:
 run(['sed','-n',f'{start},{end}p',path],m.SOURCE)
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'execution.log').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['validVerifyExit','selfTestExit','selfTestCopyModified','resealedWrongSubmittedSuccess','productionPathWrongHead','historicalManifestEntriesVerified','sourceStatus','planningStatus']},indent=2))
