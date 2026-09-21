"""Read-only checks for this sealed design pass; run from planning with source path argument."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

planning=Path.cwd()
source=Path(sys.argv[1])
project=planning/'project01-portable-persistence'
arc=project/'arc01-contract-and-mongo-pilot'
slice_root=arc/'slice02-portable-contract-design'
packet=slice_root/'artifacts/design-pass02'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((packet/'result-01.json').read_text())
attempt=json.loads((packet/'attempt-01.json').read_text())
assert result['sourceHead']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
assert subprocess.check_output(['git','status','--porcelain'],cwd=source,text=True)==''
assert attempt['attempt']==1 and attempt['exitCode']==0 and result['success']
assert attempt['protocolSha256']==sha(packet/'protocol.md')
assert result['experimentSha256']==sha(packet/'experiment.cjs')
assert sha(Path(result['compiler']['path']))==result['compiler']['sha256']
assert len(result['sources'])==5
for record in result['sources']:
    assert sha(source/record['path'])==record['sha256'],record['path']
assert len(result['cases'])==28 and all(c['passed'] for c in result['cases'])
assert all(c['candidate']['referenceLookups']==0 for c in result['cases'])
assert len(result['memoCases'])==8 and all(c['passed'] for c in result['memoCases'])
assert len(result['negativeControls'])==3 and all(c['detected'] for c in result['negativeControls'])
preserved=0
for artifact_dir in [arc/'slice01-behavior-baseline/artifacts',slice_root/'artifacts']:
    for line in (artifact_dir/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split(maxsplit=1)
        assert sha(artifact_dir/name.lstrip('*'))==digest,name
        preserved+=1
docs=[project/'project-plan.md',project/'interface-design.md',project/'operator-decisions.md',arc/'arc-plan.md',slice_root/'slice-plan.md',slice_root/'ledger.md',packet/'protocol.md',packet/'decision.md']
links=0
for doc in docs:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
        if '://' in target or target.startswith('#'):continue
        name,_,fragment=target.partition('#')
        dest=(doc.parent/name).resolve()
        assert dest.is_file(),(doc,target)
        if fragment:
            anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)}
            assert fragment in anchors,(doc,target)
        links+=1
rows=re.findall(r'^\| S\d\d \|.*$',(slice_root/'ledger.md').read_text(),re.M)
assert len(rows)==7 and all(' | open | ' in row for row in rows)
subprocess.run(['git','diff','--check'],check=True)
manifest=packet/'SHA256SUMS'
manifest_count=None
if manifest.exists():
    names=[]
    for line in manifest.read_text().splitlines():
        digest,name=line.split(maxsplit=1)
        assert sha(packet/name)==digest,name
        names.append(name)
    assert set(names)=={p.name for p in packet.iterdir() if p.is_file() and p.name!='SHA256SUMS'}
    manifest_count=len(names)
print(json.dumps({'check':'passed','sourceHead':result['sourceHead'],'sourceClean':True,'sourceFilesHashed':5,'comparisonsPassed':28,'memoCasesPassed':8,'negativeControlsDetected':3,'priorArtifactHashesPreserved':preserved,'linksAndAnchorsChecked':links,'ledgerRowsStillOpen':7,'packetManifestEntries':manifest_count,'evidenceClass':'contributor structural and mocked-store evidence; not independent or real-database acceptance'},indent=2))
