"""Read-only pass-3 evidence checks. Run from planning with source worktree argument."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
planning=Path.cwd();source=Path(sys.argv[1])
project=planning/'project01-portable-persistence'
arc=project/'arc01-contract-and-mongo-pilot'
slice=arc/'slice02-portable-contract-design'
packet=slice/'artifacts/design-pass03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((packet/'result-01.json').read_text());a=json.loads((packet/'attempt-01.json').read_text())
assert r['success'] and r['cleanedUp'] and a['exitCode']==0 and a['attempt']==1
assert a['protocolSha256']==sha(packet/'protocol.md')
assert r['experimentSha256']==a['experimentSha256']==sha(packet/'experiment.cjs')
assert r['prior']['sha256']==sha(slice/'artifacts/design-pass02/experiment.cjs')
prior=(slice/'artifacts/design-pass02/experiment.cjs').read_text()
start=prior.index('const scopeKey =');end=prior.index('const cases = [];',start)
assert r['prior']['extractedSource']==prior[start:end]
assert r['binary']['sha256']==sha(Path(r['binary']['path']))
assert r['sourceHead']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
assert subprocess.check_output(['git','status','--porcelain'],cwd=source,text=True)==''
for item in r['sourceFiles']:assert item['sha256']==sha(source/item['path'])
assert len(r['sourceFiles'])==3
assert [c['kind'] for c in r['cases']]==['unchanged','content-update','delete','recreate','rename','move']
for c in r['cases']:
    assert c['passed'] and c['same']==(c['kind'] in ['unchanged','content-update'])
    assert c['hot']['reads']==0 and c['cold']['reads']==1
    hot=next(x for x in c['links'] if x['label']=='hot')
    assert hot['physicalRowExists']==(c['kind'] not in ['delete','recreate'])
    assert hot['matchesReference']==c['same']
assert len(r['negativeControls'])==2 and all(c['detected'] for c in r['negativeControls'])
preserved=0
for folder in [arc/'slice01-behavior-baseline/artifacts',slice/'artifacts',slice/'artifacts/design-pass02']:
    for line in (folder/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split(maxsplit=1);assert sha(folder/name.lstrip('*'))==digest;preserved+=1
docs=[project/'project-plan.md',project/'interface-design.md',project/'operator-decisions.md',arc/'arc-plan.md',slice/'slice-plan.md',slice/'ledger.md',packet/'protocol.md',packet/'decision.md']
links=0
for doc in docs:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
        if '://' in target or target.startswith('#'):continue
        name,_,fragment=target.partition('#');dest=(doc.parent/name).resolve();assert dest.is_file(),(doc,target)
        if fragment:
            anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)}
            assert fragment in anchors,(doc,target)
        links+=1
rows=re.findall(r'^\| S\d\d \|.*$',(slice/'ledger.md').read_text(),re.M)
assert len(rows)==7 and all(' | open | ' in row for row in rows)
subprocess.run(['git','diff','--check'],check=True)
manifest=packet/'SHA256SUMS';count=None
if manifest.exists():
    names=[]
    for line in manifest.read_text().splitlines():
        digest,name=line.split(maxsplit=1);assert sha(packet/name)==digest;names.append(name)
    assert set(names)=={p.name for p in packet.iterdir() if p.is_file() and p.name!='SHA256SUMS'}
    count=len(names)
print(json.dumps({'check':'passed','sourceHead':r['sourceHead'],'sourceClean':True,'characterizationCases':6,'equivalenceControls':2,'equivalenceCounterexamples':4,'negativeControlsDetected':2,'priorHashesPreserved':preserved,'linksChecked':links,'openLedgerRows':7,'manifestEntries':count,'evidenceClass':'contributor synthetic Mongo primitive characterization; not integrated or independent acceptance'},indent=2))
