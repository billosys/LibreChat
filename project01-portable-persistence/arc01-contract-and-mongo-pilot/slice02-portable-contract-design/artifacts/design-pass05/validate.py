"""Read-only packet and reproducible static inventory verification."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,tempfile
root=Path.cwd();source=Path(sys.argv[1]);p=root/'project01-portable-persistence';a=p/'arc01-contract-and-mongo-pilot';s=a/'slice02-portable-contract-design';packet=s/'artifacts/design-pass05'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((packet/'result-01.json').read_text());attempt=json.loads((packet/'attempt-01.json').read_text());matrix=json.loads((packet/'field-matrix.json').read_text())
assert r['success'] and attempt['attempt']==1 and attempt['exitCode']==0
for name,digest in attempt['inputHashes'].items():assert sha(packet/name)==digest
assert sha(packet/'experiment.cjs')==r['experimentSha256']
assert r['sourceHead']==matrix['sourceHead']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
assert subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=source,text=True)==''
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=source,text=True).splitlines();assert all(n=='.AGENTS.md.swp' for n in untracked)
for f in r['sources']+matrix['sources']:assert sha(source/f['path'])==f['sha256']
assert sha(Path(r['compiler']['path']))==r['compiler']['sha256']
assert sha(s/'artifacts/design-pass04/handle.cjs')==r['priorHandle']['sha256']
assert sha(s/'artifacts/design-pass04/field-census.json')==matrix['census']['sha256']
for f in json.loads((s/'artifacts/design-pass04/field-census.json').read_text())['sources']:assert sha(source/f['path'])==f['sha256']
assert len(r['readCases'])==16 and all(c['passed'] for c in r['readCases'])
assert len(r['gateCases'])==2 and all(c['passed'] and c['responses'][0]['status']==404 for c in r['gateCases'])
assert len(r['preflightCases'])==3 and all(c['passed'] and c['direct']==c['deferred'] and c['direct']!=c['eager'] for c in r['preflightCases'])
assert r['modelAccesses']==0 and len(r['negativeControls'])==3 and all(c['detected'] for c in r['negativeControls'])
assert [len(c['fields']) for c in matrix['records']]==[44,73];assert len(matrix['exclusions'])==24 and len([x for x in matrix['exclusions'] if '.' in x])==12
with tempfile.TemporaryDirectory(prefix='guildhall-pass05-verify-') as tmp:
 dest=Path(tmp)/'matrix.json'
 subprocess.run([attempt['command'][0],str(packet/'field-matrix.cjs'),str(source),r['compiler']['path'],str(s/'artifacts/design-pass04/field-census.json'),str(dest)],check=True,stdout=subprocess.DEVNULL)
 assert dest.read_bytes()==(packet/'field-matrix.json').read_bytes()
preserved=0
for manifest in a.rglob('SHA256SUMS'):
 if manifest.parent==packet:continue
 for line in manifest.read_text().splitlines():
  digest,name=line.split(maxsplit=1);assert sha(manifest.parent/name.lstrip('*'))==digest;preserved+=1
links=0
for doc in [p/'project-plan.md',p/'interface-design.md',a/'arc-plan.md',s/'slice-plan.md',s/'ledger.md',packet/'read-contract.md',packet/'protocol.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
  if '://' in target or target.startswith('#'):continue
  name,_,fragment=target.partition('#');dest=(doc.parent/name).resolve();assert dest.is_file(),(doc,target)
  if fragment:
   anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)};assert fragment in anchors,(doc,target)
  links+=1
rows=re.findall(r'^\| S\d\d \|.*$',(s/'ledger.md').read_text(),re.M);assert len(rows)==7 and all(' | open | ' in row for row in rows)
subprocess.run(['git','diff','--check'],check=True)
manifest=packet/'SHA256SUMS';count=None
if manifest.exists():
 names=[]
 for line in manifest.read_text().splitlines():
  digest,name=line.split(maxsplit=1);assert sha(packet/name)==digest;names.append(name)
 assert set(names)=={f.name for f in packet.iterdir() if f.is_file() and f.name!='SHA256SUMS'};count=len(names)
print(json.dumps({'check':'passed','sourceHead':r['sourceHead'],'trackedSourceClean':True,'untrackedPreserved':untracked,'readComparisons':16,'admissionGatingChecks':2,'preflightCases':3,'negativeControls':3,'fieldMatrixReproduced':True,'schemaFields':117,'priorArtifactHashesPreserved':preserved,'linksChecked':links,'openLedgerRows':7,'manifestEntries':count,'evidenceClass':'source-executed read orchestration and preflight with storage doubles; static field matrix, not real-adapter or independent acceptance'},indent=2))
