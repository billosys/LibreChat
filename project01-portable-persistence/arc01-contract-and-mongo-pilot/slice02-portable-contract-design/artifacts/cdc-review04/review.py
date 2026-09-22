#!/usr/bin/env python3
"""CDC review of committed CC evidence04; writes only its output home and temp copies."""
import argparse
import collections
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PLAN = Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
SOURCE = PLAN.parent / 'billo-guildhall'
SLICE = Path('project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design')
REL = SLICE / 'artifacts/cc-evidence04'
PACKET = PLAN / REL
COMMIT = '76d15b5d33668e3c50ddd3db7b98a8e6c12a814c'
OUT = Path(sys.argv[1]).resolve()
if (OUT / 'SHA256SUMS').exists():
    raise SystemExit('Refusing to overwrite a sealed review; choose a fresh output directory.')
OUT.mkdir(parents=True, exist_ok=True)
LOG = (OUT / 'execution.log').open('w')

def emit(label, value):
    LOG.write(json.dumps({'at': datetime.now(timezone.utc).isoformat(), 'label': label, 'value': value}, sort_keys=True) + '\n')
    LOG.flush()

def run(label, argv, cwd=PLAN):
    p = subprocess.run([str(x) for x in argv], cwd=cwd, text=True, capture_output=True)
    r = {'argv': [str(x) for x in argv], 'cwd': str(cwd), 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    emit(label, r)
    return r

def git_bytes(path):
    return subprocess.check_output(['git', 'show', f'{COMMIT}:{path}'], cwd=PLAN)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def hashes():
    return {p.name: digest(p.read_bytes()) for p in PACKET.iterdir()}

before = hashes()
committed = {p.name: digest(git_bytes(REL / p.name)) for p in PACKET.iterdir()}
assert before == committed, 'working packet differs from reviewed commit'
code = git_bytes(REL / 'replay.py').decode()
ns = {'__file__': str(PACKET / 'replay.py'), '__name__': 'cdc_reviewed_cc'}
exec(compile(code, str(PACKET / 'replay.py'), 'exec'), ns)
inventory = json.loads(git_bytes(REL / 'nested-fields.json'))
baseline = json.loads(git_bytes(SLICE / 'artifacts/design-pass05/result-01.json'))
result = {'reviewedCommit': COMMIT, 'recipeSha256': digest(code.encode()), 'committedPacketMatches': before == committed}
result['source'] = {label: run(label, ['git', *args], SOURCE) for label, args in [('sourceHead', ['rev-parse', 'HEAD']), ('sourceStatus', ['status', '--short']), ('sourceBranch', ['branch', '--show-current'])]}
result['commitFiles'] = run('commit files', ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', COMMIT])
result['commitMessage'] = run('commit message', ['git', 'show', '-s', '--format=%B', COMMIT])

# Execute committed CLI bytes while keeping the pinned recipe's established path context.
wrapper = "import subprocess,sys; p=sys.argv.pop(1); c=sys.argv.pop(1); f=sys.argv.pop(1); b=subprocess.check_output(['git','show',c+':'+f],cwd=p); sys.argv[0]=p+'/'+f; exec(compile(b,p+'/'+f,'exec'),{'__file__':p+'/'+f,'__name__':'__main__'})"
def cli(label, packet, mode='--verify'):
    return run(label, [sys.executable, '-B', '-c', wrapper, PLAN, COMMIT, REL / 'replay.py', mode, '--packet', packet])

result['officialVerify'] = cli('official verify', PACKET)
result['officialSelfTest'] = cli('official self-test', PACKET, '--self-test')
result['submittedEqualsBaseline'] = json.loads(git_bytes(REL / 'replay-result.json')) == baseline

def root(inv, field):
    return next(r for r in inv['roots'] if r['field'] == field)

def file_id(inv):
    return next(m for m in root(inv, 'files')['members'] if m['path'] == 'files[].file_id')

def subset_removals(inv):
    inv['projection']['partialContainers'][0]['removed'] = ['sitelinks']

def wrong_use_site(inv):
    member = next(m for m in root(inv, 'files')['members'] if m['path'] == 'files[].filename')
    member['useSite'] = {'wrapper': 'TFile[]', 'effect': 'outer properties required at TMessage.files use site'}

mutations = [
    ('missing all retained-container obligations', lambda x: x['projection'].__setitem__('partialContainers', [])),
    ('omit organic highlights removal', subset_removals),
    ('excluded survivor plus freeform except bypass', lambda x: x['projection']['survivors'].append('content[].tool_call.backgroundTask.resultClaim except nothing')),
    ('wrong filename Partial application', wrong_use_site),
    ('wrong file_id Partial wrapper', lambda x: file_id(x)['useSite'].__setitem__('wrapper', 'TFile[]')),
    ('invented fingerprint', lambda x: x['sources'][0].__setitem__('sha256', '0' * 64)),
    ('duplicate strict path member', lambda x: root(x, 'userSubmittedMessageFieldPaths')['members'].append(copy.deepcopy(root(x, 'userSubmittedMessageFieldPaths')['members'][0]))),
    ('wrong contextMeta public view', lambda x: root(x, 'contextMeta')['applicability']['publicMessages'].__setitem__('disposition', 'fully public with every field retained')),
    ('submitted success false', None),
]
result['cliCounterexamples'] = []
for label, mutate in mutations:
    with tempfile.TemporaryDirectory(prefix='cdc-review04-') as td:
        packet = Path(td)
        for name in before:
            (packet / name).write_bytes(git_bytes(REL / name))
        filename = 'nested-fields.json' if mutate else 'replay-result.json'
        value = json.loads((packet / filename).read_text())
        if mutate:
            mutate(value)
        else:
            value['success'] = False
        (packet / filename).write_text(json.dumps(value, indent=2) + '\n')
        ns['seal'](packet)
        outcome = cli(label, packet)
        result['cliCounterexamples'].append({'name': label, 'accepted': outcome['exit'] == 0, **outcome})

# Exercise actual main/verification entrypoint with a failing environment collector.
# No real checkout/runtime is changed. Count both guard and runner calls.
calls = {'preflight': 0, 'runner': 0}
def rejected_preflight(*args, **kwargs):
    calls['preflight'] += 1
    raise ns['EvidenceError']('CDC injected source-head mismatch')
def runner(*args, **kwargs):
    calls['runner'] += 1
    return copy.deepcopy(baseline)
old_preflight, old_runner, old_argv = ns['preflight'], ns['harness_result'], sys.argv
ns['preflight'], ns['harness_result'] = rejected_preflight, runner
sys.argv = ['replay.py', '--verify', '--packet', str(PACKET)]
try:
    status = ns['main']()
    gate = {'accepted': status == 0, 'status': status, 'calls': calls}
except Exception as e:
    gate = {'accepted': False, 'error': str(e), 'calls': calls}
finally:
    ns['preflight'], ns['harness_result'], sys.argv = old_preflight, old_runner, old_argv
result['preflightCounterexample'] = gate
emit('injected preflight at actual main', gate)

with tempfile.TemporaryDirectory(prefix='cdc-review04-runner-mutation-') as td:
    packet = Path(td)
    for name in before:
        (packet / name).write_bytes(git_bytes(REL / name))
    def mutating_runner():
        (packet / 'report.md').write_text('CDC disposable mutation during verification\n')
        return copy.deepcopy(baseline)
    try:
        ns['validate_packet'](packet, runner=mutating_runner)
        mutation_result = {'accepted': True}
    except Exception as e:
        mutation_result = {'accepted': False, 'error': str(e)}
    result['duringVerificationMutation'] = mutation_result
    emit('packet mutation during verification', mutation_result)

# Compare coverage against the independently reviewed prior packet, not the new builder.
previous = json.loads(git_bytes(SLICE / 'artifacts/cc-evidence03/nested-fields.json'))
prior_by_key = {(r['record'], r['field']): r['classification'] for r in previous['coverage']}
result['classificationCounts'] = dict(collections.Counter(r['classification'] for r in inventory['coverage']))
result['classificationDifferences'] = [dict(r, expectedClassification=prior_by_key[(r['record'], r['field'])]) for r in inventory['coverage'] if r['classification'] != prior_by_key[(r['record'], r['field'])]]
result['roots'] = [{'record': r['record'], 'field': r['field'], 'applicability': r['applicability'], 'memberCount': len(r['members']), 'paths': [m['path'] for m in r['members']]} for r in inventory['roots']]
result['declaredSymbols'] = [d['symbol'] for d in inventory['declarations']]
result['fileSourcesPresent'] = any(d['symbol'] == 'FileSources' for d in inventory['declarations'])
result['fileContextPresent'] = any(d['symbol'] == 'FileContext' for d in inventory['declarations'])
result['sourceFingerprintChecks'] = [{'path': x['path'], 'matches': digest((SOURCE / x['path']).read_bytes()) == x['sha256']} for x in inventory['sources']]
result['sourceWitnesses'] = []
for rel, start, end in [
    ('packages/data-provider/src/schemas.ts', 1016, 1075),
    ('packages/data-provider/src/types/content.ts', 187, 315),
    ('packages/data-provider/src/types/files.ts', 1, 43),
    ('packages/data-provider/src/types/files.ts', 137, 224),
    ('packages/data-provider/src/types/web.ts', 19, 58),
    ('packages/data-provider/src/types/web.ts', 90, 94),
    ('packages/data-provider/src/codeEnvRef.ts', 41, 80),
    ('packages/data-schemas/src/methods/message.ts', 456, 482),
    ('packages/data-schemas/src/methods/conversation.ts', 2060, 2078),
]:
    raw = (SOURCE / rel).read_bytes()
    witness = {'path': rel, 'sourceHead': result['source']['sourceHead']['stdout'].strip(), 'sha256': digest(raw), 'lines': [start, end], 'text': '\n'.join(raw.decode().splitlines()[start-1:end])}
    result['sourceWitnesses'].append(witness)
    emit('source witness', witness)

matrix = json.loads(git_bytes(SLICE / 'artifacts/design-pass05/field-matrix.json'))
query = run('independent complete matrix projection', ['jq', '-c', '.records[] | {name, fields: [.fields[].name], providerOnly, interfaceOnly, implicit}', PLAN / SLICE / 'artifacts/design-pass05/field-matrix.json'])
observed = [json.loads(line) for line in query['stdout'].splitlines()]
expected = [dict(name=r['name'], fields=[f['name'] for f in r['fields']], providerOnly=r['providerOnly'], interfaceOnly=r['interfaceOnly'], implicit=r['implicit']) for r in matrix['records']]
logged_queries = [e for e in (json.loads(line) for line in git_bytes(REL / 'execution.log').decode().splitlines()) if e.get('kind') == 'command' and e.get('argv', [])[:2] == ['jq', '-c']]
result['matrixProjection'] = {'freshMatchesCommitted': observed == expected, 'captureQueryCount': len(logged_queries), 'eachCaptureMatches': [ [json.loads(line) for line in e['stdout'].splitlines()] == expected for e in logged_queries], 'counts': [{'name': r['name'], 'fields': len(r['fields']), 'providerOnly': len(r['providerOnly']), 'interfaceOnly': len(r['interfaceOnly']), 'implicit': len(r['implicit'])} for r in observed]}

# Validate exactly the manifests present at the reviewed commit, including old packets.
tree = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', COMMIT, 'project01-portable-persistence'], cwd=PLAN, text=True).splitlines()
manifest_checks = []
for manifest in (p for p in tree if p.endswith('/SHA256SUMS')):
    for line in git_bytes(manifest).decode().splitlines():
        if not line.strip():
            continue
        expected, name = line.split(maxsplit=1)
        target = (Path(manifest).parent / name.lstrip('*')).as_posix()
        manifest_checks.append({'manifest': manifest, 'path': target, 'matches': digest((PLAN / target).read_bytes()) == expected})
result['manifestChecks'] = manifest_checks
result['manifestEntryCount'] = len(manifest_checks)
result['packetPreserved'] = hashes() == before
result['sourceStatusAfter'] = run('source status after', ['git', 'status', '--short'], SOURCE)
result['planningStatusAfter'] = run('planning status after', ['git', 'status', '--short'])
(OUT / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
emit('summary', {'packetPreserved': result['packetPreserved'], 'manifestEntries': len(manifest_checks), 'counterexamplesAccepted': sum(x['accepted'] for x in result['cliCounterexamples']), 'preflight': gate})
LOG.close()
print(json.dumps({'officialVerifyExit': result['officialVerify']['exit'], 'officialSelfTestExit': result['officialSelfTest']['exit'], 'packetPreserved': result['packetPreserved'], 'manifestEntryCount': len(manifest_checks), 'badManifestEntries': sum(not x['matches'] for x in manifest_checks), 'classificationCounts': result['classificationCounts'], 'classificationDifferences': len(result['classificationDifferences']), 'counterexamples': [{'name': x['name'], 'accepted': x['accepted']} for x in result['cliCounterexamples']], 'preflight': gate}, indent=2))
