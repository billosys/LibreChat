import copy,hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
PLAN=Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
S=PLAN/'project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design'
P=S/'artifacts/cc-evidence03';OUT=Path('/tmp/guildhall-cdc-review03');OUT.mkdir(exist_ok=True)
COMMIT='0f81e318bdd78619b5092c188c5149ae5178de35';records=[]
def run(argv,cwd=PLAN):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,text=True,capture_output=True);r=dict(argv=list(map(str,argv)),cwd=str(cwd),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr);records.append(r);return r
def hashes(p):return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.iterdir()) if f.is_file()}
before=hashes(P);result={'reviewedCommit':COMMIT,'packetBefore':before}
for name,h in before.items():assert hashlib.sha256(subprocess.check_output(['git','show',COMMIT+':'+str((P/name).relative_to(PLAN))],cwd=PLAN)).hexdigest()==h
assert set(run(['git','diff-tree','--no-commit-id','--name-only','-r',COMMIT])['stdout'].splitlines())=={str((P/n).relative_to(PLAN)) for n in before}
message=run(['git','show','-s','--format=%B',COMMIT])['stdout']
for footer in ['Co-authored-by: Codex <noreply@openai.com>','Co-authored-by: Billo AI <ai-engineering@billo.systems>']:assert message.count(footer)==1
for mode in ['--verify','--self-test']:
 r=run([sys.executable,P/'replay.py',mode,'--packet',P]);result[mode]={'exitCode':r['exitCode'],'output':json.loads(r['stdout']) if r['exitCode']==0 else r['stderr']};assert r['exitCode']==0
assert hashes(P)==before
spec=importlib.util.spec_from_file_location('cc03',P/'replay.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
j=m.read_json(P/'nested-fields.json');matrix=m.read_json(m.MATRIX)
result['actualSubmittedMatchesBaseline']=m.read_json(P/'replay-result.json')==m.read_json(m.SEALED_RESULT);assert result['actualSubmittedMatchesBaseline']
declarations_record=run([m.NODE,Path(__file__).with_name('declarations.cjs'),m.SOURCE,m.COMPILER]);assert declarations_record['exitCode']==0
declarations=json.loads(declarations_record['stdout'])
result['sourceDeclarationExtraction']={'kind':declarations['kind'],'count':len(declarations['declarations']),'symbols':[{'file':d['file'],'symbol':d['symbol'],'start':d['start'],'end':d['end']} for d in declarations['declarations']]}
result['syntaxOnlyOracle']={d['symbol']:d['properties'] for d in declarations['declarations'] if d['symbol'] in ['userSubmittedMessageFieldPathSchema','tExampleSchema','subagentThreadLineageSchema','SummaryContentPart']}
# Discriminating whole-projection control: this sibling is excluded by a DIFFERENT entry.
bad=copy.deepcopy(j);e=next(e for e in bad['nestedExclusions'] if e['path']=='content.tool_call.backgroundTask.completionWakeup');e['permittedSiblings'][0]['path']='content[].tool_call.backgroundTask.resultClaim'
try:m.validate_inventory(bad,matrix);result['otherExclusionControl']={'rejected':False,'mutation':'completionWakeup permitted sibling changed to resultClaim'}
except m.EvidenceError as exc:result['otherExclusionControl']={'rejected':True,'error':str(exc)}
# Independent actual CLI controls, resealed on temporary copies.
result['submittedCLIControls']=[]
with tempfile.TemporaryDirectory(prefix='cdc03-result-controls-') as d:
 for key,value in [('success',False),('node','v0.invalid')]:
  def mutate(target,key=key,value=value):
   v=m.read_json(target/'replay-result.json');v[key]=value;(target/'replay-result.json').write_text(json.dumps(v)+'\n')
  c=m.seal_copy(P,Path(d)/key,mutate);r=run([sys.executable,P/'replay.py','--verify','--packet',c]);result['submittedCLIControls'].append({'key':key,'value':value,'exitCode':r['exitCode'],'rejected':r['exitCode']!=0,'stderr':r['stderr']});assert r['exitCode']!=0
# Reproduce complete data queries with independent exact equality checks.
result['matrixQueries']={}
for name in ['messageSchema','convoSchema']:
 r=run(['jq','-c',f'.records[] | select(.name=="{name}") | {{name,fields,providerOnly,interfaceOnly,implicit}}',m.MATRIX]);v=json.loads(r['stdout']);base=next(x for x in matrix['records'] if x['name']==name)
 assert all(v[k]==base[k] for k in ['name','fields','providerOnly','interfaceOnly','implicit'])
 result['matrixQueries'][name]={'fields':len(v['fields']),'uniqueFields':len({x['name'] for x in v['fields']}),'providerOnly':len(v['providerOnly']),'interfaceOnly':len(v['interfaceOnly']),'implicit':list(v['implicit']),'exactSelectedData':True}
selected={'metadata.codeEnvRef','content[].tool_call.backgroundTask.settledAt','content[].error.text','content[].summary.boundary.contentIndex','files[].file_id','files[].metadata.codeEnvRef','attachments[].variant2.expiresAt','userSubmittedMessageFieldPaths[].source','examples[].input.role','subagentThread.parentAgentId'}
result['inventorySemantics']={r['field']:{'applicability':r['applicability'],'selectedMembers':[x for x in r['members'] if x['path'] in selected]} for r in j['roots']}
# Recover actual committed query outputs, not just the corrected driver source.
log_text=(P/'execution.log').read_text();decoder=json.JSONDecoder();found={};offset=0
while offset<len(log_text):
 if log_text[offset] not in '{[':offset+=1;continue
 try:value,end=decoder.raw_decode(log_text,offset)
 except json.JSONDecodeError:offset+=1;continue
 def walk(value):
  if isinstance(value,dict):
   if 'argv' in value and 'stdout' in value:
    for name in ['messageSchema','convoSchema']:
     if any(f'select(.name=="{name}")' in arg for arg in value['argv']):
      try:projected=json.loads(value['stdout'])
      except json.JSONDecodeError:continue
      if isinstance(projected,dict) and projected.get('name')==name and 'fields' in projected:found[name]=projected
   for child in value.values():walk(child)
  elif isinstance(value,list):
   for child in value:walk(child)
 walk(value);offset=end
assert set(found)=={'messageSchema','convoSchema'}
for name,value in found.items():assert value['fields']==next(row['fields'] for row in matrix['records'] if row['name']==name)
result['committedQueryOutputsMatchMatrix']={name:len(value['fields']) for name,value in found.items()}

result['memberStatistics']={'total':sum(len(r['members']) for r in j['roots']),'placeholderDeclaredType':sum(x['declaredType']=='declared local type; see sourceRefs' for r in j['roots'] for x in r['members'])}
# Check actual composed-exclusion membership independently of CC's local-pair predicate.
blocked=sorted(m.canonical(x) for x in m.EXCLUSION_KEYS);violations=[];partial_containers=[]
for e in j['nestedExclusions']:
 for survivor in e['permittedSiblings']:
  path=m.canonical(survivor['path'])
  for b in blocked:
   if path[:len(b)]==b:violations.append({'entry':e['path'],'survivor':survivor['path'],'blocked':'.'.join(b)})
   elif b[:len(path)]==path:partial_containers.append({'entry':e['path'],'survivingContainer':survivor['path'],'nestedExclusion':'.'.join(b)})
result['actualCrossExclusionViolations']=violations
result['partiallyRetainedContainers']=partial_containers
result['reviewerMethodCorrection']='Initial ancestor-prefix scan identified 18 container/exclusion pairs. Those containers legitimately survive with filtered children; this final scan separates them from directly excluded paths. No claim of 18 erroneous survivors is made.'
source_ranges=[('packages/data-provider/src/types/content.ts',195,315),('packages/data-provider/src/feedback.ts',22,29),('packages/data-provider/src/schemas.ts',1016,1061),('packages/data-provider/src/codeEnvRef.ts',1,77),('packages/data-provider/src/types/web.ts',88,96),('packages/data-provider/src/filters.ts',184,191),('packages/data-provider/src/schemas.ts',867,876),('packages/data-provider/src/schemas.ts',1102,1138),('packages/data-provider/src/types/agents.ts',81,135),('packages/data-provider/src/types/files.ts',150,221),('packages/data-provider/src/types/web.ts',19,58),('packages/data-schemas/src/methods/message.ts',456,481),('packages/data-schemas/src/methods/conversation.ts',2060,2078),('packages/data-schemas/src/types/message.ts',68,96)]
for path,start,end in source_ranges:assert run(['sed','-n',f'{start},{end}p',path],m.SOURCE)['exitCode']==0
manifest_paths=run(['git','ls-tree','-r','--name-only',COMMIT,'--','project01-portable-persistence'])['stdout'].splitlines();verified=[]
for rel in manifest_paths:
 if Path(rel).name!='SHA256SUMS':continue
 f=PLAN/rel
 for line in f.read_text().splitlines():
  if not line.strip():continue
  expected,name=line.split(None,1);q=f.parent/name.lstrip('*');assert hashlib.sha256(q.read_bytes()).hexdigest()==expected;qrel=str(q.relative_to(PLAN));verified.append(qrel)
result['historicalManifestEntriesVerified']=len(verified);result['historicalFiles']=verified
result['sourceStatus']=run(['git','status','--porcelain','--untracked-files=all'],m.SOURCE)['stdout'];assert result['sourceStatus']==''
result['planningStatus']=run(['git','status','--porcelain','--untracked-files=all'])['stdout'];result['packetAfter']=hashes(P);assert before==result['packetAfter']
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'execution.log').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({'verifyExit':result['--verify']['exitCode'],'selfTestExit':result['--self-test']['exitCode'],'negativeRejections':result['--self-test']['output']['rejections'],'otherExclusionControl':result['otherExclusionControl'],'actualCrossExclusionViolations':violations,'matrixQueries':result['matrixQueries'],'historicalHashes':len(verified),'packetUnchanged':before==hashes(P)},indent=2))
