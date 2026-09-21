from pathlib import Path
import subprocess,hashlib,json,copy,tempfile,sys
PLAN=Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
SOURCE=PLAN.parent/'billo-guildhall'
REL=Path('project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design')
SLICE=PLAN/REL
SUBJECT='99d5ecd794d00cd1c0db7a199633042766af5953'
out=Path(sys.argv[1])
if (out/'SHA256SUMS').exists():raise SystemExit('Refusing to rewrite a sealed review packet; use a fresh temporary output directory')
out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log=[]
def run(args,cwd):
 r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 log.append({'argv':args,'cwd':str(cwd),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 return r
try:
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()=='3e3c5410d3863118fdba694fb0cd51baeb7102f9'
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=SOURCE,text=True)
 cc=SLICE/'artifacts/cc-evidence01';before={p.name:sha(p) for p in cc.iterdir() if p.is_file()};assert len(before)==7
 changes=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',SUBJECT],cwd=PLAN,text=True).splitlines()
 assert set(changes)=={str(REL/'artifacts/cc-evidence01'/name) for name in before}
 hashes=0
 manifest_paths=subprocess.check_output(['git','ls-tree','-r','--name-only',SUBJECT,'--','project01-portable-persistence/arc01-contract-and-mongo-pilot'],cwd=PLAN,text=True).splitlines()
 for name in manifest_paths:
  if not name.endswith('/SHA256SUMS'):continue
  manifest=PLAN/name
  committed=subprocess.check_output(['git','show',SUBJECT+':'+name],cwd=PLAN,text=True)
  assert manifest.read_text()==committed
  for line in committed.splitlines():
   digest,name=line.split(maxsplit=1);assert sha(manifest.parent/name.lstrip('*'))==digest;hashes+=1
 assert hashes==87
 matrix=json.loads((SLICE/'artifacts/design-pass05/field-matrix.json').read_text());inventory=json.loads((cc/'nested-fields.json').read_text());original=json.loads((cc/'replay-result.json').read_text())
 expected={('message' if rec['name']=='messageSchema' else 'conversation',f['name']):f for rec in matrix['records'] for f in rec['fields']}
 rows={(r['record'],r['field']):r for r in inventory['coverage']}
 assert set(rows)==set(expected) and len(rows)==len(inventory['coverage'])==117
 roots={('message',f) for f in ['content','files','attachments','metadata','feedback','contextMeta','userSubmittedMessageFieldPaths']}|{('conversation',f) for f in ['examples','codeWorkspaces','subagentThread']}
 assert {(r['record'],r['field']) for r in inventory['roots']}==roots and len(inventory['roots'])==10
 for key,entry in expected.items():
  label='selected nested root' if key in roots else 'adapter-private physical relationship' if key==('conversation','messages') else 'default-hidden specialized field' if entry['defaultRead']=='hidden' else 'other scalar/array field outside this deep inspection'
  assert rows[key]['classification']==label
 exclusions={x for x in matrix['exclusions'] if '.' in x};assert len(exclusions)==12
 assert {x['path'] for x in inventory['nestedExclusions']}==exclusions and len(inventory['nestedExclusions'])==12
 for s in inventory['sources']:assert sha(SOURCE/s['path'])==s['sha256']
 with tempfile.TemporaryDirectory(prefix='guildhall-cdc-replay-') as temp:
  dest=Path(temp)/'result.json'
  args=['/Users/oubiwann/.local/bin/node',str(SLICE/'artifacts/design-pass05/experiment.cjs'),str(SOURCE),'/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js',str(SLICE/'artifacts/design-pass04/handle.cjs'),str(dest)]
  r=run(args,PLAN);assert r.returncode==0
  actual=json.loads(dest.read_text());assert actual==original
 # Load the committed verifier as a library, never its writing main().
 subject_path=str(REL/'artifacts/cc-evidence01/replay.py')
 raw=subprocess.check_output(['git','show',SUBJECT+':'+subject_path],cwd=PLAN)
 namespace={'__name__':'cdc_readonly_subject','__file__':str(cc/'replay.py')};exec(compile(raw,subject_path,'exec'),namespace)
 controls=[]
 for field,value in [('node','v0.invalid'),('sourceHead','0'*40),('compiler',{**original['compiler'],'sha256':'0'*64})]:
  changed=copy.deepcopy(original);changed[field]=value
  try:
   result=namespace['compare_results'](changed,original);controls.append({'mutation':field,'rejected':False,'returned':result})
  except AssertionError as e:controls.append({'mutation':field,'rejected':True,'error':str(e)})
 changed=copy.deepcopy(inventory);changed['coverage'][0]['classification']='invalid-unclassified'
 try:
  result=namespace['validate_inventory'](changed,matrix);classification_control={'rejected':False,'returned':result}
 except AssertionError as e:classification_control={'rejected':True,'error':str(e)}
 assert before=={p.name:sha(p) for p in cc.iterdir() if p.is_file()}
 result={'subjectCommit':SUBJECT,'sourceHead':actual['sourceHead'],'replayExactlyMatchesCC':True,'readCases':len(actual['readCases']),'gateCases':len(actual['gateCases']),'preflightCases':len(actual['preflightCases']),'negativeControls':len(actual['negativeControls']),'coverageFields':len(rows),'selectedRoots':len(roots),'nestedExclusions':len(exclusions),'sourceFingerprintsChecked':len(inventory['sources']),'artifactHashesVerified':hashes,'subjectVerifierSha256':hashlib.sha256(raw).hexdigest(),'verifierProvenanceControls':controls,'verifierClassificationControl':classification_control,'ccPacketUnchanged':True,'evidenceLimits':'Replay of existing storage-double harness and independent structural checks. Semantic review is separately recorded; no integrated Mongo/build acceptance.'}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if not k.startswith('verifier')},indent=2));print('Provenance controls rejected:',[x['rejected'] for x in controls]);print('Invalid classification rejected:',classification_control['rejected'])
finally:
 (out/'execution.log').write_text(json.dumps(log,indent=2)+'\n')
