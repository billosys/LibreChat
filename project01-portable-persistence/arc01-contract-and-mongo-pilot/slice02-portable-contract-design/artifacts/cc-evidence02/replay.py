#!/usr/bin/env python3
"""Fail-closed capture, read-only verification, and self-tests for CC evidence02."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

PLAN = Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
SOURCE = Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall')
SLICE = PLAN / 'project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design'
DEFAULT_PACKET = SLICE / 'artifacts/cc-evidence02'
SEALED = SLICE / 'artifacts/design-pass05'
PRIOR = SLICE / 'artifacts/design-pass04'
MATRIX = SEALED / 'field-matrix.json'
SEALED_RESULT = SEALED / 'result-01.json'
NODE = Path('/Users/oubiwann/.local/bin/node')
COMPILER = Path('/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js')
EXPECTED_SOURCE_HEAD = '3e3c5410d3863118fdba694fb0cd51baeb7102f9'
EXPECTED_SOURCE_BRANCH = 'billo-guildhall'
EXPECTED_NODE = 'v22.22.3'
EXPECTED_COMPILER_VERSION = '5.9.3'
EXPECTED_COMPILER_SHA = '3ae902c92cc44dace175c0e69e13a4b0899f6983c6121d76b9ab8dd5795e7675'
EXPECTED_EXPERIMENT_SHA = 'f33bdd87b9691fdfb26adebb4e058fdb641f50e0be596f6f9e9d8c80b0037339'
EXPECTED_HANDLE_SHA = 'b1efac13c8c2aa1d1a23c2fb8bf3d209673abcb3da798164da49bfab99bcabc4'
EXPECTED_PROMPT_SHA = 'cd8bdf9db78247d4a15d14ff76106e1e0ce74a45a8b765097bbfeba23bd6904d'
EXPECTED_PRIOR_PACKET_MANIFEST_SHA = '6a7aaa9bbae775461ff81615bf8026c36cc10172b0f77657340a9ba85fd0dc3b'
EXPECTED_CDC_REVIEW_RESULT_SHA = 'f7117ee576164dd0161d0ea41f46457fbc5ca18fd9b802f165febdaf42d806a9'
EXPECTED_MANIFESTS = {
    'artifacts/SHA256SUMS': '9a154519192f951b2036c3c4263634bf6815de61a2919e98bba3a8fafeecafff',
    'artifacts/design-pass02/SHA256SUMS': 'f027b20a65290a3c74f6a212241629c23f99d8be75d2aacd580334f76d7cf79f',
    'artifacts/design-pass03/SHA256SUMS': 'dc2348c81b9bb4aafed25600329d14047e1cadf5f7305f52b6aeed7cf2070a77',
    'artifacts/design-pass04/SHA256SUMS': '34b5c312e5a522916f857a9f1dba6fd8c6d6868c2aed35d9062182d04e7453c8',
    'artifacts/design-pass05/SHA256SUMS': '515e47b1d388ef3f8bb5d42ff258da0ea340b37c5e8d7e64bc6c6396b05e4c68',
}
OLD_INPUT_HASHES = {
    'artifacts/design-pass05/read-contract.md': '3aec3158c4e888640124ac446fff02e06fc4e1ff6ea2d1d90ab0dab09365d99e',
    'artifacts/design-pass05/protocol.md': 'e2c45e56558d9434d61fa110344c80748a00dcfb5482cc3aab4635732e339339',
    'artifacts/design-pass05/experiment.cjs': EXPECTED_EXPERIMENT_SHA,
    'artifacts/design-pass05/field-matrix.cjs': '8cbb81dee30eab0a58dc96ec1db2e65f0c4e4ca5266e1501accf7bb42b8fb6f4',
    'artifacts/design-pass05/validate.py': '6fb512a7d3564e5c96206cef1f0b7855147f25c75e144e6f90c4ef46d6debb9b',
    'artifacts/design-pass05/field-matrix.json': 'c1e32f81a7a105dc32e2f036ffeb08688c5c362e57e5b038d4ea3cd4e6806ab1',
    'artifacts/design-pass05/result-01.json': 'e01753920035301d3ac18ad53ea0f577e7129504f618fa357234f9e855cee367',
    'artifacts/design-pass04/handle.cjs': EXPECTED_HANDLE_SHA,
    'artifacts/design-pass04/field-census.json': '845eb74a93285be66a6072f23a3468ab7fbd258000b687f9ebe2fe5db77b806f',
}
BEHAVIOR_FIELDS = ['readCases', 'gateCases', 'preflightCases', 'negativeControls', 'success', 'modelAccesses', 'error']
PROVENANCE_FIELDS = ['sourceHead', 'node', 'compiler', 'sources', 'experimentSha256', 'priorHandle']
PACKET_FILES = {'intake.md', 'report.md', 'nested-fields.json', 'replay-result.json', 'execution.log', 'replay.py', 'SHA256SUMS'}
ROOT_KEYS = {('message', x) for x in ('content', 'files', 'attachments', 'metadata', 'feedback', 'contextMeta', 'userSubmittedMessageFieldPaths')} | {('conversation', x) for x in ('examples', 'codeWorkspaces', 'subagentThread')}
EXCLUSION_KEYS = {'metadata.thoughtSignatures', 'content.tool_call.backgroundTask.resultClaim', 'content.tool_call.backgroundTask.completionWakeup', 'attachments.web_search.knowledgeGraph', 'attachments.web_search.peopleAlsoAsk', 'attachments.web_search.relatedSearches', 'attachments.web_search.shopping', 'attachments.web_search.places', 'attachments.web_search.news', 'attachments.web_search.organic.sitelinks', 'attachments.web_search.organic.highlights', 'attachments.web_search.topStories.highlights'}

class EvidenceError(RuntimeError):
    """A prerequisite or submitted-evidence predicate failed."""

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))

def append_log(packet: Path, title: str, value: Any) -> None:
    log = packet / 'execution.log'
    if not log.exists():
        log.write_text('# CC evidence02 execution log\nAppend-only commands, controls, and structural checks.\n', encoding='utf-8')
    with log.open('a', encoding='utf-8') as stream:
        stream.write(f'\n[{stamp()}] {title}\n')
        stream.write(value if isinstance(value, str) else json.dumps(value, indent=2))
        stream.write('\n')

def run_record(argv: list[str], cwd: Path) -> dict[str, Any]:
    started = stamp()
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    return {'argv': argv, 'cwd': str(cwd), 'startedAt': started, 'finishedAt': stamp(), 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}

def command_or_error(argv: list[str], cwd: Path, label: str) -> dict[str, Any]:
    record = run_record(argv, cwd)
    if record['exitCode'] != 0:
        raise EvidenceError(f'{label} failed with exit {record["exitCode"]}: {record["stderr"]}')
    return record

def git_value(args: list[str]) -> str:
    return subprocess.check_output(['git', *args], cwd=SOURCE, text=True).strip()

def collect_environment() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    branch = command_or_error(['git', 'branch', '--show-current'], SOURCE, 'source branch')
    head = command_or_error(['git', 'rev-parse', 'HEAD'], SOURCE, 'source head')
    status = command_or_error(['git', 'status', '--porcelain', '--untracked-files=all'], SOURCE, 'source status')
    node = command_or_error([str(NODE), '--version'], PLAN, 'node version')
    compiler = command_or_error([str(NODE), '-e', f"console.log(require({json.dumps(str(COMPILER))}).version)"], PLAN, 'compiler version')
    values = {'branch': branch['stdout'].strip(), 'sourceHead': head['stdout'].strip(), 'sourceStatus': status['stdout'], 'node': node['stdout'].strip(), 'compilerVersion': compiler['stdout'].strip(), 'compilerSha256': digest(COMPILER)}
    return values, [branch, head, status, node, compiler]

def expected_label(record: str, field: str, baseline: dict[tuple[str, str], dict[str, Any]]) -> str:
    if (record, field) in ROOT_KEYS:
        return 'selected nested root'
    if (record, field) == ('conversation', 'messages'):
        return 'adapter-private physical relationship'
    if baseline[(record, field)]['defaultRead'] == 'hidden':
        return 'default-hidden specialized field'
    return 'other scalar/array field outside this deep inspection'

def check_ref(source_ref: dict[str, Any], label: str) -> None:
    required = {'path', 'lines', 'symbol', 'kind', 'observation'}
    if not required <= set(source_ref) or not isinstance(source_ref['lines'], list) or len(source_ref['lines']) != 2:
        raise EvidenceError(f'{label}: malformed source reference')
    path = SOURCE / source_ref['path']
    if not path.is_file():
        raise EvidenceError(f'{label}: missing source file {source_ref["path"]}')
    start, end = source_ref['lines']
    line_count = sum(1 for _ in path.open(encoding='utf-8'))
    if not isinstance(start, int) or not isinstance(end, int) or start < 1 or start > end or end > line_count:
        raise EvidenceError(f'{label}: line bounds {source_ref["lines"]} outside {source_ref["path"]}:{line_count}')

def check_refs(value: Any, label: str) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        if {'path', 'lines', 'symbol', 'kind', 'observation'} <= set(value):
            check_ref(value, label)
            paths.add(value['path'])
        for key, item in value.items():
            paths.update(check_refs(item, f'{label}.{key}'))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.update(check_refs(item, f'{label}[{index}]'))
    return paths

def validate_inventory(inventory: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    required = {'sourceHead', 'sources', 'coverage', 'roots', 'nestedExclusions', 'unresolved'}
    if not required <= set(inventory):
        raise EvidenceError(f'inventory missing top-level keys: {sorted(required - set(inventory))}')
    baseline = {(('message' if record['name'] == 'messageSchema' else 'conversation'), field['name']): field for record in matrix['records'] for field in record['fields']}
    rows = [(row['record'], row['field']) for row in inventory['coverage']]
    if len(rows) != 117 or len(set(rows)) != 117 or set(rows) != set(baseline):
        raise EvidenceError('coverage membership, denominator, or uniqueness mismatch')
    for row in inventory['coverage']:
        if row['classification'] != expected_label(row['record'], row['field'], baseline):
            raise EvidenceError(f'classification mismatch for {row["record"]}.{row["field"]}')
    actual_roots = {(root['record'], root['field']) for root in inventory['roots']}
    if actual_roots != ROOT_KEYS or len(inventory['roots']) != 10:
        raise EvidenceError('selected root membership mismatch')
    source_paths = {item['path'] for item in inventory['sources']}
    if len(source_paths) != len(inventory['sources']) or inventory['sourceHead'] != EXPECTED_SOURCE_HEAD:
        raise EvidenceError('source fingerprint identity mismatch')
    for item in inventory['sources']:
        path = SOURCE / item['path']
        if not path.is_file() or digest(path) != item['sha256']:
            raise EvidenceError(f'source fingerprint mismatch: {item["path"]}')
    referenced = check_refs(inventory['roots'], 'roots') | check_refs(inventory['nestedExclusions'], 'nestedExclusions')
    if not referenced <= source_paths:
        raise EvidenceError(f'cited sources missing from fingerprint list: {sorted(referenced - source_paths)}')
    for root in inventory['roots']:
        if not root.get('members') or set(root.get('applicability', {})) != {'serverHistory', 'publicMessages', 'turnConversation', 'accessProbe'}:
            raise EvidenceError(f'incomplete nested map for {root["record"]}.{root["field"]}')
        for member in root['members']:
            if not {'path', 'arrayBoundary', 'storageDomain', 'serverDomain', 'providerDomain', 'requiredness', 'default', 'nullEvidence', 'openBoundary', 'sourceRefs'} <= set(member):
                raise EvidenceError(f'incomplete member row in {root["field"]}')
        for name, disposition in root['applicability'].items():
            if disposition.get('status') not in {'established', 'not applicable', 'not established'} or not disposition.get('reason'):
                raise EvidenceError(f'incomplete applicability {root["field"]}.{name}')
            if disposition['status'] == 'established' and not disposition.get('sourceRefs'):
                raise EvidenceError(f'established applicability lacks source ref {root["field"]}.{name}')
        if not root.get('witnesses'):
            raise EvidenceError(f'missing witnesses for {root["field"]}')
        for witness in root['witnesses']:
            if witness['kind'] == 'bounded-search':
                if not witness.get('searchSurface') or not witness.get('query') or not witness.get('result'):
                    raise EvidenceError(f'incomplete bounded search witness {root["field"]}')
            elif not {'path', 'symbol', 'lines', 'observation'} <= set(witness):
                raise EvidenceError(f'incomplete source witness {root["field"]}')
    if {item['path'] for item in inventory['nestedExclusions']} != EXCLUSION_KEYS or len(inventory['nestedExclusions']) != 12:
        raise EvidenceError('nested exclusion membership mismatch')
    for exclusion in inventory['nestedExclusions']:
        if not exclusion.get('traversal') or not exclusion.get('removedMember') or not exclusion.get('permittedSiblings') or not exclusion.get('sourceRefs'):
            raise EvidenceError(f'incomplete nested exclusion {exclusion.get("path")}')
    if not inventory['unresolved'] or any(item.get('owner') != 'CDC' for item in inventory['unresolved']):
        raise EvidenceError('unresolved decision ownership mismatch')
    counts = {}
    for row in inventory['coverage']:
        counts[row['classification']] = counts.get(row['classification'], 0) + 1
    return {'coverageRows': len(rows), 'uniqueCoverageKeys': len(set(rows)), 'selectedRoots': len(inventory['roots']), 'nestedExclusions': len(inventory['nestedExclusions']), 'classificationCounts': counts, 'sourceFingerprints': len(source_paths)}

def verify_old_inputs() -> dict[str, Any]:
    manifests = {}
    for relative, expected in EXPECTED_MANIFESTS.items():
        path = SLICE / relative
        if digest(path) != expected:
            raise EvidenceError(f'historical manifest drift: {relative}')
        manifests[relative] = expected
    inputs = {}
    for relative, expected in OLD_INPUT_HASHES.items():
        path = SLICE / relative
        if digest(path) != expected:
            raise EvidenceError(f'pinned input drift: {relative}')
        inputs[relative] = expected
    return {'manifestSet': manifests, 'inputSet': inputs, 'scope': 'explicit pass02-pass05 manifests and pass05/pass04 replay inputs; no global recursive denominator'}

def verify_prior_packets() -> dict[str, Any]:
    prior_manifest = SLICE / 'artifacts/cc-evidence01/SHA256SUMS'
    if digest(prior_manifest) != EXPECTED_PRIOR_PACKET_MANIFEST_SHA:
        raise EvidenceError('cc-evidence01 manifest drift')
    entries = {}
    for line in prior_manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        value, name = line.split(maxsplit=1)
        entries[name.lstrip('*')] = value
    expected_names = PACKET_FILES - {'SHA256SUMS'}
    if set(entries) != expected_names:
        raise EvidenceError('cc-evidence01 manifest membership drift')
    for name, value in entries.items():
        path = prior_manifest.parent / name
        if not path.is_file() or digest(path) != value:
            raise EvidenceError(f'cc-evidence01 packet hash drift: {name}')
    review_result = SLICE / 'artifacts/cdc-review01/result.json'
    if digest(review_result) != EXPECTED_CDC_REVIEW_RESULT_SHA:
        raise EvidenceError('cdc-review01 result drift')
    result = read_json(review_result)
    controls = result.get('verifierProvenanceControls', [])
    if len(controls) != 3 or not all(item.get('rejected') is False for item in controls) or result.get('verifierClassificationControl', {}).get('rejected') is not False:
        raise EvidenceError('CDC review controls are not the reviewed four-control result')
    return {'priorManifestSha256': digest(prior_manifest), 'priorPacketEntries': entries, 'cdcReviewResultSha256': digest(review_result), 'cdcReviewControls': 4}

def verify_environment(inventory: dict[str, Any], observed: dict[str, Any] | None = None, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    if observed is None:
        observed, _ = collect_environment()
    values = copy.deepcopy(observed)
    if overrides:
        values.update(overrides)
    expected = {'branch': EXPECTED_SOURCE_BRANCH, 'sourceHead': EXPECTED_SOURCE_HEAD, 'sourceStatus': '', 'node': EXPECTED_NODE, 'compilerVersion': EXPECTED_COMPILER_VERSION, 'compilerSha256': EXPECTED_COMPILER_SHA}
    for key, expected_value in expected.items():
        if values.get(key) != expected_value:
            raise EvidenceError(f'preflight mismatch {key}: {values.get(key)!r} != {expected_value!r}')
    source_overrides = values.get('sourceDigestOverrides', {})
    for source in inventory['sources']:
        actual = source_overrides.get(source['path'], digest(SOURCE / source['path']))
        if actual != source['sha256']:
            raise EvidenceError(f'inventory source fingerprint mismatch at execution: {source["path"]}')
    return {'environment': {key: values[key] for key in expected}, 'oldInputs': verify_old_inputs(), 'priorPackets': verify_prior_packets(), 'inventorySourcesChecked': len(inventory['sources'])}

def exact_compare(actual: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    for field in BEHAVIOR_FIELDS + PROVENANCE_FIELDS:
        actual_present = field in actual
        expected_present = field in expected
        if actual_present != expected_present:
            raise EvidenceError(f'comparison key presence mismatch in {field}; absent and null are distinct')
        if actual_present and actual[field] != expected[field]:
            raise EvidenceError(f'exact comparison mismatch in {field}')
    return {'behaviorFieldsExact': BEHAVIOR_FIELDS, 'provenanceFieldsExact': PROVENANCE_FIELDS, 'allowedDifferences': []}

def packet_hashes(packet: Path) -> dict[str, str]:
    return {name: digest(packet / name) for name in sorted(PACKET_FILES) if (packet / name).is_file()}

def verify_manifest(packet: Path) -> dict[str, str]:
    manifest = packet / 'SHA256SUMS'
    if not manifest.is_file():
        raise EvidenceError('packet is not sealed: SHA256SUMS missing')
    entries = {}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        value, name = line.split(maxsplit=1)
        entries[name.lstrip('*')] = value
    expected = PACKET_FILES - {'SHA256SUMS'}
    if set(entries) != expected:
        raise EvidenceError(f'packet manifest membership mismatch: {sorted(set(entries) ^ expected)}')
    for name, value in entries.items():
        if not (packet / name).is_file() or digest(packet / name) != value:
            raise EvidenceError(f'packet hash mismatch: {name}')
    return entries

def packet_inputs(packet: Path, sealed: bool) -> dict[str, Any]:
    if not packet.is_absolute():
        raise EvidenceError('packet path must be absolute')
    if not packet.is_dir():
        raise EvidenceError(f'packet directory missing: {packet}')
    names = {path.name for path in packet.iterdir() if path.is_file()}
    if sealed:
        if names != PACKET_FILES:
            raise EvidenceError(f'sealed packet inventory mismatch: {sorted(names ^ PACKET_FILES)}')
        verify_manifest(packet)
    else:
        if 'SHA256SUMS' in names:
            raise EvidenceError('capture refuses a destination that already has SHA256SUMS')
        required = {'intake.md', 'report.md', 'nested-fields.json', 'replay.py'}
        if not required <= names:
            raise EvidenceError(f'capture inputs missing: {sorted(required - names)}')
        if not names <= (required | {'replay-result.json', 'execution.log'}):
            raise EvidenceError(f'capture destination has unexpected files: {sorted(names - required - {"replay-result.json", "execution.log"})}')
    return {'packetFiles': sorted(names), 'sealed': sealed}

def fresh_query(packet: Path) -> list[dict[str, Any]]:
    jq = shutil.which('jq')
    rg = shutil.which('rg')
    if jq is None or rg is None:
        raise EvidenceError('required jq/rg executable is missing')
    records = []
    matrix = str(MATRIX)
    prior_result = str(SLICE / 'artifacts/cc-evidence01/replay-result.json')
    prior_inventory = str(SLICE / 'artifacts/cc-evidence01/nested-fields.json')
    review_result = str(SLICE / 'artifacts/cdc-review01/result.json')
    queries = [
        [jq, '-c', '{sourceHead,exclusions,providerOnly,interfaceOnly,implicit}', matrix],
        [jq, '-c', '[.records[]|select(.name=="messageSchema")|.fields[]]', matrix],
        [jq, '-c', '[.records[]|select(.name=="conversationSchema")|.fields[]]', matrix],
        [jq, '-c', '{roots,nestedExclusions}', prior_inventory],
        [jq, '-c', '{readCases,gateCases}', prior_result],
        [jq, '-c', '{preflightCases,negativeControls,success,modelAccesses,error}', prior_result],
        [jq, '-c', '{sourceHead,node,compiler,sources,experimentSha256,priorHandle}', prior_result],
        [jq, '-c', '.', review_result],
    ]
    for argv in queries:
        record = run_record(argv, PLAN)
        if record['exitCode'] not in (0, 1):
            raise EvidenceError(f'required data query failed: {argv}')
        records.append(record)
    surfaces = ['api/app/clients', 'api/server/routes/messages.js', 'api/server/controllers/agents', 'packages/api/src/conversations', 'packages/api/src/agents/hitl', 'packages/data-provider/src']
    for term in ['content', 'files', 'attachments', 'metadata', 'feedback', 'contextMeta', 'userSubmittedMessageFieldPaths', 'examples', 'codeWorkspaces', 'subagentThread']:
        records.append(run_record([rg, '-n', '--no-heading', '-F', term, *surfaces], SOURCE))
    ranges = [
        ('packages/data-provider/src/types/web.ts', 19, 60), ('packages/data-provider/src/types/web.ts', 403, 421),
        ('packages/data-provider/src/types/agents.ts', 81, 145), ('packages/data-provider/src/types/files.ts', 150, 221),
        ('packages/data-schemas/src/methods/conversation.ts', 2060, 2078), ('packages/data-schemas/src/schema/message.ts', 103, 121),
        ('packages/data-schemas/src/schema/message.ts', 138, 151), ('packages/data-schemas/src/schema/message.ts', 238, 247),
        ('packages/data-schemas/src/schema/convo.ts', 52, 65), ('packages/data-schemas/src/schema/defaults.ts', 30, 35),
        ('packages/data-schemas/src/schema/defaults.ts', 327, 336), ('packages/data-schemas/src/schema/fading.ts', 19, 34),
        ('packages/data-provider/src/schemas.ts', 867, 876), ('packages/data-provider/src/schemas.ts', 1039, 1069),
        ('packages/data-provider/src/schemas.ts', 1102, 1113), ('packages/data-provider/src/schemas.ts', 1127, 1136),
        ('packages/data-provider/src/feedback.ts', 103, 145), ('packages/data-provider/src/filters.ts', 184, 191),
        ('packages/data-provider/src/types/content.ts', 244, 315), ('packages/data-schemas/src/methods/message.ts', 456, 481),
        ('packages/data-schemas/src/methods/message.ts', 939, 975), ('api/server/routes/messages.js', 232, 360),
        ('api/server/routes/messages.js', 565, 705), ('api/server/controllers/agents/client.js', 2249, 2320),
    ]
    for path, start, end in ranges:
        records.append(run_record(['sed', '-n', f'{start},{end}p', path], SOURCE))
    append_log(packet, 'fresh required-data queries, bounded witness searches, and selected enclosing reads', records)
    return records

def harness_command(output: Path) -> list[str]:
    return [str(NODE), str(SEALED / 'experiment.cjs'), str(SOURCE), str(COMPILER), str(PRIOR / 'handle.cjs'), str(output)]

def run_capture(packet: Path) -> dict[str, Any]:
    packet_inputs(packet, sealed=False)
    inventory = read_json(packet / 'nested-fields.json')
    matrix = read_json(MATRIX)
    structural = validate_inventory(inventory, matrix)
    observed, records = collect_environment()
    preflight = verify_environment(inventory, observed)
    append_log(packet, 'capture preflight commands and predicates', {'commands': records, 'preflight': preflight, 'structural': structural})
    fresh_query(packet)
    result_path = packet / 'replay-result.json'
    if result_path.exists():
        append_log(packet, 'prior replay bytes preserved before capture replacement', result_path.read_text(encoding='utf-8'))
    replay = run_record(harness_command(result_path), PLAN)
    append_log(packet, 'pass05 replay', replay)
    if replay['exitCode'] != 0:
        if result_path.exists():
            append_log(packet, 'failed replay result retained before stopping', result_path.read_text(encoding='utf-8'))
        raise EvidenceError('pass05 replay failed; no success was fabricated')
    actual = read_json(result_path)
    comparison = exact_compare(actual, read_json(SEALED_RESULT))
    append_log(packet, 'exact replay comparison', comparison)
    validator = run_record([sys.executable, str(SEALED / 'validate.py'), str(SOURCE)], PLAN)
    append_log(packet, 'sealed pass05 validator', validator)
    if validator['exitCode'] != 0:
        raise EvidenceError('sealed pass05 validator failed')
    return {'structural': structural, 'preflight': preflight, 'replay': replay, 'comparison': comparison, 'validator': validator}

def verify_packet(packet: Path, injected_runner: Callable[[], tuple[dict[str, Any], dict[str, Any]]] | None = None) -> dict[str, Any]:
    packet_inputs(packet, sealed=True)
    before = packet_hashes(packet)
    inventory = read_json(packet / 'nested-fields.json')
    structural = validate_inventory(inventory, read_json(MATRIX))
    observed, environment_commands = collect_environment()
    preflight = verify_environment(inventory, observed)
    with tempfile.TemporaryDirectory(prefix='cc-evidence02-verify-') as temporary:
        output = Path(temporary) / 'replay-result.json'
        if injected_runner is None:
            record = run_record(harness_command(output), PLAN)
            actual = read_json(output) if output.exists() else None
        else:
            record, actual = injected_runner()
        if record['exitCode'] != 0:
            raise EvidenceError('verification harness failed')
        if actual is None:
            raise EvidenceError('verification harness produced no result')
        comparison = exact_compare(actual, read_json(SEALED_RESULT))
    after = packet_hashes(packet)
    if before != after:
        raise EvidenceError('packet hash changed during read-only verification')
    return {'mode':'verify','packetBefore':before,'environmentCommands':environment_commands,'structural':structural,'preflight':preflight,'harness':record,'comparison':comparison,'packetAfter':after,'packetUnchanged':True}

def expect_rejection(label: str, thunk: Callable[[], Any]) -> dict[str, Any]:
    try:
        thunk()
    except EvidenceError as error:
        return {'control':label,'rejected':True,'error':str(error)}
    except AssertionError as error:
        return {'control':label,'rejected':True,'error':str(error)}
    return {'control':label,'rejected':False}

def self_test(packet: Path) -> dict[str, Any]:
    if not packet.is_dir() or not (packet / 'nested-fields.json').is_file() or not (packet / 'replay-result.json').is_file():
        raise EvidenceError('self-test requires a captured packet')
    inventory = read_json(packet / 'nested-fields.json')
    matrix = read_json(MATRIX)
    valid = validate_inventory(inventory, matrix)
    base, _ = collect_environment()
    controls = [
        expect_rejection('wrong-runtime', lambda: verify_environment(inventory, base, {'node':'v0.invalid'})),
        expect_rejection('wrong-source-head', lambda: verify_environment(inventory, base, {'sourceHead':'0' * 40})),
        expect_rejection('wrong-compiler-digest', lambda: verify_environment(inventory, base, {'compilerSha256':'0' * 64})),
        expect_rejection('wrong-source-file-digest', lambda: verify_environment(inventory, base, {'sourceDigestOverrides':{inventory['sources'][0]['path']:'0' * 64}})),
    ]
    sentinel = {'calls': 0}
    def preflight_sentinel() -> dict[str, Any]:
        sentinel['calls'] += 1
        return {'argv':['preflight-sentinel'],'cwd':str(PLAN),'startedAt':stamp(),'finishedAt':stamp(),'exitCode':0,'stdout':'','stderr':''}
    controls.append(expect_rejection('preflight-runner-sentinel', lambda: (verify_environment(inventory, base, {'sourceHead':'0' * 40}), preflight_sentinel())))
    bad_classification = copy.deepcopy(inventory); bad_classification['coverage'][0]['classification'] = 'invalid-unclassified'
    controls.append(expect_rejection('invalid-classification', lambda: validate_inventory(bad_classification, matrix)))
    missing = copy.deepcopy(inventory); missing['coverage'].pop()
    controls.append(expect_rejection('missing-field', lambda: validate_inventory(missing, matrix)))
    duplicate = copy.deepcopy(inventory); duplicate['coverage'].append(copy.deepcopy(duplicate['coverage'][0]))
    controls.append(expect_rejection('duplicate-field', lambda: validate_inventory(duplicate, matrix)))
    sealed = read_json(SEALED_RESULT)
    missing_key = copy.deepcopy(sealed); missing_key.pop('sourceHead', None)
    null_key = copy.deepcopy(sealed); null_key['sourceHead'] = None
    controls.append(expect_rejection('absent-provenance-key', lambda: exact_compare(missing_key, sealed)))
    controls.append(expect_rejection('null-provenance-key', lambda: exact_compare(null_key, sealed)))
    if 'error' not in sealed:
        missing_behavior = copy.deepcopy(sealed); null_behavior = copy.deepcopy(sealed); null_behavior['error'] = None
        controls.append(expect_rejection('absent-behavior-key', lambda: exact_compare(missing_behavior, null_behavior)))
        controls.append(expect_rejection('null-behavior-key', lambda: exact_compare(null_behavior, missing_behavior)))
    with tempfile.TemporaryDirectory(prefix='cc-evidence02-selftest-') as temporary:
        temporary_packet = Path(temporary) / 'sealed'
        temporary_packet.mkdir()
        for name in PACKET_FILES - {'SHA256SUMS'}:
            shutil.copy2(packet / name, temporary_packet / name)
        (temporary_packet / 'SHA256SUMS').write_text('\n'.join(f'{digest(temporary_packet / name)}  {name}' for name in sorted(PACKET_FILES - {'SHA256SUMS'})) + '\n')
        before = packet_hashes(temporary_packet)
        controls.append(expect_rejection('capture-sealed-destination', lambda: packet_inputs(temporary_packet, sealed=False)))
        def injected_runner() -> tuple[dict[str, Any], dict[str, Any]]:
            return {'argv':['self-test-injected-harness'],'cwd':str(PLAN),'startedAt':stamp(),'finishedAt':stamp(),'exitCode':0,'stdout':'','stderr':''}, sealed
        verify_packet(temporary_packet, injected_runner=injected_runner)
        controls.append({'control':'verify-packet-hash-preservation','rejected':before == packet_hashes(temporary_packet),'packetUnchanged':before == packet_hashes(temporary_packet)})
    if sentinel['calls'] != 0:
        raise EvidenceError('preflight runner sentinel was invoked')
    if not all(item.get('rejected') for item in controls):
        raise EvidenceError('one or more self-test controls failed to reject drift')
    result = {'validControl': valid, 'controls': controls, 'runnerSentinel': {'calls': sentinel['calls'], 'expectedCalls': 0, 'passed': sentinel['calls'] == 0}}
    append_log(packet, 'self-test controls before sealing', result)
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description='CC evidence02 capture/verify/self-test driver')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--capture', action='store_true')
    modes.add_argument('--verify', action='store_true')
    modes.add_argument('--self-test', action='store_true')
    parser.add_argument('--packet', type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args()
    if not any((args.capture, args.verify, args.self_test)):
        parser.print_usage(sys.stderr)
        return 2
    try:
        if args.capture:
            result = run_capture(args.packet)
        elif args.verify:
            result = verify_packet(args.packet)
        else:
            result = self_test(args.packet)
        print(json.dumps(result, indent=2))
        return 0
    except (EvidenceError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(json.dumps({'mode':'capture' if args.capture else 'verify' if args.verify else 'self-test','success':False,'blocked':True,'error':str(error)}, indent=2), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
