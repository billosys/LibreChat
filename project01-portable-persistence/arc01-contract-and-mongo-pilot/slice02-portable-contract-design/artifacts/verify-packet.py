"""Read-only structural self-check. Run from the canonical planning checkout."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

root = Path.cwd()
source = Path('/Users/oubiwann/lab/billosys/LibreChat')
arc = root / 'project01-portable-persistence/arc01-contract-and-mongo-pilot'
slice_root = arc / 'slice02-portable-contract-design'
artifacts = slice_root / 'artifacts'
baseline = arc / 'slice01-behavior-baseline/artifacts'
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
assert head == 'ba44443fdb232bbe6d4977e2619774b5a72586ac'
status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=source, text=True)
assert status == '', status
counts = {}
for manifest in ('source-fingerprints.json', 'dist-fingerprints.json'):
    entries = json.loads((baseline / manifest).read_text())
    for entry in entries:
        assert sha(source / entry['path']) == entry['sha256'], entry['path']
    counts[manifest] = len(entries)
prior_hashes = 0
for line in (baseline / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    path = baseline / name.lstrip('*')
    assert sha(path) == digest, name
    prior_hashes += 1

result = json.loads((artifacts / 'pagination-result.json').read_text())
attempt = json.loads((artifacts / 'pagination-attempt.json').read_text())
assert attempt['attempt'] == 1 and attempt['exitCode'] == 0
assert attempt['protocolSha256'] == sha(artifacts / 'pagination-protocol.md')
assert result['harnessSucceeded'] and result['cleanedUp'] and result['defaultPortRejected']
assert result['sourceHead'] == head
for entry in result['artifacts']:
    path = Path(entry['file'])
    if path.name == 'pagination-harness.cjs':
        path = artifacts / path.name
    assert sha(path) == entry['sha256'], path
control, tied = result['trials']
assert control['storedCount'] == 6 and control['returnedCount'] == 6 and control['completenessPassed']
assert tied['storedCount'] == 6 and tied['returnedCount'] == 4 and len(tied['missing']) == 2
assert not tied['completenessPassed'] and not tied['duplicates'] and not tied['extra']
assert control['termination'] == tied['termination'] == 'exhausted'

docs = [root/'README.md', root/'project01-portable-persistence/project-plan.md',
        root/'project01-portable-persistence/ledger.md',
        root/'project01-portable-persistence/interface-design.md',
        arc/'arc-plan.md', arc/'ledger.md', *slice_root.rglob('*.md')]
links = 0
for doc in docs:
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', doc.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        filename, _, fragment = target.partition('#')
        destination = (doc.parent / filename).resolve()
        assert destination.is_file(), (doc, target)
        if fragment:
            headers = re.findall(r'^#+\s+(.+)$', destination.read_text(), re.M)
            anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headers}
            assert fragment in anchors, (doc, target, anchors)
        links += 1
ledger_rows = re.findall(r'^\| S\d\d \|.*$', (slice_root/'ledger.md').read_text(), re.M)
assert len(ledger_rows) == 7
assert all(' | open | ' in row for row in ledger_rows)
subprocess.run(['git', 'diff', '--check'], cwd=root, check=True)
packet_hashes = None
if (artifacts / 'SHA256SUMS').exists():
    lines = (artifacts / 'SHA256SUMS').read_text().splitlines()
    listed = set()
    for line in lines:
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        assert sha(artifacts / name) == digest, name
        listed.add(name)
    assert listed == {str(p.relative_to(artifacts)) for p in artifacts.rglob('*') if p.is_file() and p.name != 'SHA256SUMS'}
    packet_hashes = len(lines)
print(json.dumps({'selfCheck': 'passed', 'sourceHead': head, 'sourceClean': True,
    'sourceAndDistFingerprints': counts, 'priorPacketHashes': prior_hashes,
    'relativeFileLinksAndAnchors': links, 'sliceLedgerRowsOpen': len(ledger_rows),
    'experimentAttempts': 1, 'fixtureCompleteness': {'unique': '6/6 pass', 'tied': '4/6 fail'},
    'currentPacketHashes': packet_hashes, 'independentVerification': False}, indent=2))
