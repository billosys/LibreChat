"""Read-only structural validation; source and planning paths are explicit."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,tempfile
planning=Path.cwd();source=Path(sys.argv[1]);p=planning/'project01-portable-persistence';a=p/'arc01-contract-and-mongo-pilot';s=a/'slice02-portable-contract-design';packet=s/'artifacts/design-pass04'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
r=json.loads((packet/'result-01.json').read_text());attempt=json.loads((packet/'attempt-01.json').read_text());census=json.loads((packet/'field-census.json').read_text())
assert r['success'] and attempt['attempt']==1 and attempt['exitCode']==0
for name,digest in attempt['inputHashes'].items():assert sha(packet/name)==digest
assert r['experimentSha256']==sha(packet/'experiment.cjs') and r['handleSha256']==sha(packet/'handle.cjs')
assert r['sourceHead']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
assert subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=source,text=True)==''
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=source,text=True).splitlines()
assert all(name=='.AGENTS.md.swp' for name in untracked),untracked
for f in r['sources']+census['sources']:assert sha(source/f['path'])==f['sha256']
assert len(r['sources'])==7 and len(census['sources'])==5
assert sha(Path(r['compiler']['path']))==r['compiler']['sha256']
assert len(r['cases'])==28 and all(x['passed'] for x in r['cases'])
for c in r['cases']:
 assert c['candidate']['referenceLookups']==0
 assert all(h['released'] and not h['retainsLocator'] for h in c['candidate']['handles'])
assert len(r['lifecycleCases'])==26 and all(x['passed'] for x in r['lifecycleCases'])
assert len(r['negativeControls'])==5 and all(x['detected'] for x in r['negativeControls'])
assert [len(x['fields']) for x in census['records']]==[44,73]
with tempfile.TemporaryDirectory(prefix='guildhall-census-validation-') as tmp:
 dest=Path(tmp)/'census.json'
 subprocess.run([attempt['command'][0],str(packet/'field-census.cjs'),str(source),r['compiler']['path'],str(dest)],check=True,stdout=subprocess.DEVNULL)
 assert dest.read_bytes()==(packet/'field-census.json').read_bytes()
preserved=0
for folder in [a/'slice01-behavior-baseline/artifacts',s/'artifacts',s/'artifacts/design-pass02',s/'artifacts/design-pass03']:
 for line in (folder/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split(maxsplit=1);assert sha(folder/name.lstrip('*'))==digest;preserved+=1
docs=[p/'project-plan.md',p/'interface-design.md',a/'arc-plan.md',s/'slice-plan.md',s/'ledger.md',packet/'protocol.md',packet/'decision.md',packet/'contract-mapping.md'];links=0
for doc in docs:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
  if '://' in target or target.startswith('#'):continue
  name,_,fragment=target.partition('#');dest=(doc.parent/name).resolve();assert dest.is_file(),(doc,target)
  if fragment:
   anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)}
   assert fragment in anchors,(doc,target)
  links+=1
rows=re.findall(r'^\| S\d\d \|.*$',(s/'ledger.md').read_text(),re.M);assert len(rows)==7 and all(' | open | ' in row for row in rows)
subprocess.run(['git','diff','--check'],check=True)
manifest=packet/'SHA256SUMS';count=None
if manifest.exists():
 names=[]
 for line in manifest.read_text().splitlines():
  digest,name=line.split(maxsplit=1);assert sha(packet/name)==digest;names.append(name)
 assert set(names)=={f.name for f in packet.iterdir() if f.is_file() and f.name!='SHA256SUMS'};count=len(names)
print(json.dumps({'check':'passed','sourceHead':r['sourceHead'],'trackedSourceClean':True,'untrackedFilesPreserved':untracked,'orchestrationComparisons':28,'lifecycleChecks':26,'negativeControls':5,'schemaFields':[44,73],'censusReproduced':True,'priorArtifactHashesPreserved':preserved,'linksChecked':links,'openLedgerRows':7,'manifestEntries':count,'evidenceClass':'contributor source-executed orchestration with mocked stores and static schema inventory; not independent or integrated database acceptance'},indent=2))
