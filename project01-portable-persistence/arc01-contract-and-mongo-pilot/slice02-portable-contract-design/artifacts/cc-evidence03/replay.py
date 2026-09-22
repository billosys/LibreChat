#!/usr/bin/env python3
"""Iteration02 evidence capture, read-only verification, and controls."""

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
DEFAULT_PACKET = SLICE / 'artifacts/cc-evidence03'
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
EXPECTED_PROMPT_SHA = 'c0b4f94e2954dde39f9265c465f4dea9a46934fb7f24ebabac56f365102a4d51'
EXPECTED_EVIDENCE01_MANIFEST_SHA = '6a7aaa9bbae775461ff81615bf8026c36cc10172b0f77657340a9ba85fd0dc3b'
EXPECTED_EVIDENCE02_MANIFEST_SHA = '9b53fcbcfec705d26af66051b0a34c9947249055bba88ebc920bab6db2c3cb8e'
EXPECTED_CDC_REVIEW01_SHA = 'f7117ee576164dd0161d0ea41f46457fbc5ca18fd9b802f165febdaf42d806a9'
EXPECTED_CDC_REVIEW02_SHA = '0d119df11ff117512e46ac4728e32b98bdac26dcede7d81c301ba23fd960d0be'
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
APPLICABILITY_KEYS = {'serverHistory', 'publicMessages', 'turnConversation', 'accessProbe'}


class EvidenceError(RuntimeError):
    """A submitted evidence predicate failed."""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def append_log(packet: Path, title: str, value: Any) -> None:
    log = packet / 'execution.log'
    if not log.exists():
        log.write_text('# CC evidence03 execution log\nAppend-only commands, controls, and structural checks.\n', encoding='utf-8')
    with log.open('a', encoding='utf-8') as stream:
        stream.write(f'\n[{stamp()}] {title}\n')
        stream.write(value if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True))
        stream.write('\n')


def run_record(argv: list[str], cwd: Path) -> dict[str, Any]:
    started = stamp()
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    return {'argv': argv, 'cwd': str(cwd), 'startedAt': started, 'finishedAt': stamp(), 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def record_then_check(packet: Path, title: str, record: dict[str, Any], allowed: set[int] = {0}) -> dict[str, Any]:
    append_log(packet, title, record)
    if record['exitCode'] not in allowed:
        raise EvidenceError(f'{title} failed with exit {record["exitCode"]}: {record["stderr"]}')
    return record


def command_or_error(argv: list[str], cwd: Path, label: str) -> dict[str, Any]:
    record = run_record(argv, cwd)
    if record['exitCode'] != 0:
        raise EvidenceError(f'{label} failed with exit {record["exitCode"]}: {record["stderr"]}')
    return record


def collect_environment() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    commands = [
        command_or_error(['git', 'branch', '--show-current'], SOURCE, 'source branch'),
        command_or_error(['git', 'rev-parse', 'HEAD'], SOURCE, 'source head'),
        command_or_error(['git', 'status', '--porcelain', '--untracked-files=all'], SOURCE, 'source status'),
        command_or_error([str(NODE), '--version'], PLAN, 'node version'),
        command_or_error([str(NODE), '-e', f"console.log(require({json.dumps(str(COMPILER))}).version)"], PLAN, 'compiler version'),
    ]
    values = {
        'branch': commands[0]['stdout'].strip(),
        'sourceHead': commands[1]['stdout'].strip(),
        'sourceStatus': commands[2]['stdout'],
        'node': commands[3]['stdout'].strip(),
        'compilerVersion': commands[4]['stdout'].strip(),
        'compilerSha256': digest(COMPILER),
    }
    return values, commands


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


def canonical(path: str) -> tuple[str, ...]:
    return tuple(part.replace('[]', '') for part in path.split('.') if part)


def expected_label(record: str, field: str, baseline: dict[tuple[str, str], dict[str, Any]]) -> str:
    if (record, field) in ROOT_KEYS:
        return 'selected nested root'
    if (record, field) == ('conversation', 'messages'):
        return 'adapter-private physical relationship'
    if baseline[(record, field)]['defaultRead'] == 'hidden':
        return 'default-hidden specialized field'
    return 'other scalar/array field outside this deep inspection'


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
            raise EvidenceError(f'inventory source fingerprint mismatch: {item["path"]}')
    referenced = check_refs(inventory['roots'], 'roots') | check_refs(inventory['nestedExclusions'], 'nestedExclusions')
    if not referenced <= source_paths:
        raise EvidenceError(f'cited sources missing from fingerprint list: {sorted(referenced - source_paths)}')
    for root in inventory['roots']:
        if len(root.get('members', [])) < 3 or set(root.get('applicability', {})) != APPLICABILITY_KEYS:
            raise EvidenceError(f'incomplete nested map for {root["record"]}.{root["field"]}')
        member_paths = {item.get('path') for item in root['members']}
        for item in root['members']:
            if not {'path', 'arrayBoundary', 'storageDomain', 'serverDomain', 'providerDomain', 'declaredType', 'declarationContext', 'requiredness', 'default', 'nullEvidence', 'openBoundary', 'sourceRefs'} <= set(item):
                raise EvidenceError(f'incomplete member row in {root["field"]}')
            if not item['sourceRefs']:
                raise EvidenceError(f'member lacks source refs in {root["field"]}.{item["path"]}')
        for name, disposition in root['applicability'].items():
            if disposition.get('status') not in {'established', 'not applicable', 'not established'} or not disposition.get('reason') or 'disposition' not in disposition:
                raise EvidenceError(f'incomplete applicability {root["field"]}.{name}')
            if disposition['status'] == 'established' and not disposition.get('sourceRefs'):
                raise EvidenceError(f'established applicability lacks source ref {root["field"]}.{name}')
        if not root.get('witnesses'):
            raise EvidenceError(f'missing witnesses for {root["field"]}')
        for witness in root['witnesses']:
            if witness.get('kind') == 'bounded-search':
                if not witness.get('searchSurface') or not witness.get('query') or not witness.get('result'):
                    raise EvidenceError(f'incomplete bounded search witness {root["field"]}')
            elif not {'path', 'symbol', 'lines', 'observation'} <= set(witness):
                raise EvidenceError(f'incomplete source witness {root["field"]}')
        required_paths = {
            'content': {'content[].tool_call.backgroundTask.settledAt', 'content[].tool_call.backgroundTask.resultClaim.claimId', 'content[].tool_call.approval.allowed_decisions[]', 'content[].summary.boundary.contentIndex'},
            'files': {'files[].file_id', 'files[].expiresAt', 'files[].metadata.runFile', 'files[].metadata.codeEnvRef'},
            'attachments': {'attachments[].web_search.organic[].sitelinks[]', 'attachments[].file_search.organic[]', 'attachments[].expiresAt', 'attachments[].variant1.file_id', 'attachments[].variant2.expiresAt', 'attachments[].variant3.conversationId'},
            'metadata': {'metadata.thoughtSignatures', 'metadata.codeEnvRef'},
            'feedback': {'feedback.rating', 'feedback.tag', 'feedback.tag.key', 'feedback.tag.direction'},
            'contextMeta': {'contextMeta.fading.v', 'contextMeta.fading.budgetTokens', 'contextMeta.fading.masked', 'contextMeta.fadingTiers[].agentId'},
            'userSubmittedMessageFieldPaths': {'userSubmittedMessageFieldPaths[].path', 'userSubmittedMessageFieldPaths[].source'},
            'examples': {'examples[].input.content', 'examples[].output.content'},
            'codeWorkspaces': {'codeWorkspaces[].environmentId', 'codeWorkspaces[].workspaceId'},
            'subagentThread': {'subagentThread.rootConversationId', 'subagentThread.parentToolCallId', 'subagentThread.subagentKind', 'subagentThread.depth'},
        }
        if not required_paths[root['field']] <= member_paths:
            raise EvidenceError(f'local member expansion incomplete for {root["field"]}: {sorted(required_paths[root["field"]] - member_paths)}')
    if {item['path'] for item in inventory['nestedExclusions']} != EXCLUSION_KEYS or len(inventory['nestedExclusions']) != 12:
        raise EvidenceError('nested exclusion membership mismatch')
    for exclusion in inventory['nestedExclusions']:
        if not exclusion.get('traversal') or exclusion.get('removedMember') != exclusion.get('path') or not exclusion.get('permittedSiblings') or not exclusion.get('sourceRefs'):
            raise EvidenceError(f'incomplete nested exclusion {exclusion.get("path")}')
        blocked = canonical(exclusion['path'])
        for sibling in exclusion['permittedSiblings']:
            survivor = canonical(sibling['path'])
            if survivor[:len(blocked)] == blocked or blocked[:len(survivor)] == survivor:
                raise EvidenceError(f'permitted sibling is covered by exclusion: {exclusion["path"]} <- {sibling["path"]}')
            if not sibling.get('sourceRefs'):
                raise EvidenceError(f'permitted sibling lacks source refs: {sibling["path"]}')
    if not inventory['unresolved'] or any(item.get('owner') != 'CDC' for item in inventory['unresolved']):
        raise EvidenceError('unresolved decision ownership mismatch')
    counts: dict[str, int] = {}
    for row in inventory['coverage']:
        counts[row['classification']] = counts.get(row['classification'], 0) + 1
    return {'coverageRows': len(rows), 'uniqueCoverageKeys': len(set(rows)), 'selectedRoots': len(inventory['roots']), 'nestedExclusions': len(inventory['nestedExclusions']), 'classificationCounts': counts, 'sourceFingerprints': len(source_paths), 'memberCounts': {root['field']: len(root['members']) for root in inventory['roots']}}


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


def manifest_entries(path: Path) -> dict[str, str]:
    entries = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            value, name = line.split(maxsplit=1)
            entries[name.lstrip('*')] = value
    return entries


def verify_packet_manifest(path: Path, expected_sha: str, required_names: set[str]) -> dict[str, Any]:
    if digest(path) != expected_sha:
        raise EvidenceError(f'prior packet manifest drift: {path}')
    entries = manifest_entries(path)
    if set(entries) != required_names:
        raise EvidenceError(f'prior packet manifest membership drift: {path}')
    for name, value in entries.items():
        target = path.parent / name
        if not target.is_file() or digest(target) != value:
            raise EvidenceError(f'prior packet hash drift: {path.parent}/{name}')
    return {'manifestSha256': expected_sha, 'entries': entries}


def verify_prior_packets() -> dict[str, Any]:
    six = PACKET_FILES - {'SHA256SUMS'}
    one = verify_packet_manifest(SLICE / 'artifacts/cc-evidence01/SHA256SUMS', EXPECTED_EVIDENCE01_MANIFEST_SHA, six)
    two = verify_packet_manifest(SLICE / 'artifacts/cc-evidence02/SHA256SUMS', EXPECTED_EVIDENCE02_MANIFEST_SHA, six)
    review01 = SLICE / 'artifacts/cdc-review01/result.json'
    review02 = SLICE / 'artifacts/cdc-review02/result.json'
    if digest(review01) != EXPECTED_CDC_REVIEW01_SHA or digest(review02) != EXPECTED_CDC_REVIEW02_SHA:
        raise EvidenceError('CDC review result drift')
    return {'evidence01': one, 'evidence02': two, 'cdcReview01Sha256': EXPECTED_CDC_REVIEW01_SHA, 'cdcReview02Sha256': EXPECTED_CDC_REVIEW02_SHA}


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


def exact_compare(actual: dict[str, Any], expected: dict[str, Any], label: str = 'comparison') -> dict[str, Any]:
    for field in BEHAVIOR_FIELDS + PROVENANCE_FIELDS:
        actual_present = field in actual
        expected_present = field in expected
        if actual_present != expected_present:
            raise EvidenceError(f'{label}: key presence mismatch in {field}; absent and null are distinct')
        if actual_present and actual[field] != expected[field]:
            raise EvidenceError(f'{label}: exact value mismatch in {field}')
    return {'label': label, 'behaviorFieldsExact': BEHAVIOR_FIELDS, 'provenanceFieldsExact': PROVENANCE_FIELDS, 'allowedDifferences': []}


def packet_hashes(packet: Path) -> dict[str, str]:
    return {name: digest(packet / name) for name in sorted(PACKET_FILES) if (packet / name).is_file()}


def verify_manifest(packet: Path) -> dict[str, str]:
    manifest = packet / 'SHA256SUMS'
    if not manifest.is_file():
        raise EvidenceError('packet is not sealed: SHA256SUMS missing')
    entries = manifest_entries(manifest)
    expected = PACKET_FILES - {'SHA256SUMS'}
    if set(entries) != expected:
        raise EvidenceError(f'packet manifest membership mismatch: {sorted(set(entries) ^ expected)}')
    for name, value in entries.items():
        if not (packet / name).is_file() or digest(packet / name) != value:
            raise EvidenceError(f'packet hash mismatch: {name}')
    return entries


def packet_inputs(packet: Path, sealed: bool) -> dict[str, Any]:
    if not packet.is_absolute() or not packet.is_dir():
        raise EvidenceError(f'packet directory missing or non-absolute: {packet}')
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
        if not names <= required | {'replay-result.json', 'execution.log'}:
            raise EvidenceError(f'capture destination has unexpected files: {sorted(names - required - {"replay-result.json", "execution.log"})}')
    return {'packetFiles': sorted(names), 'sealed': sealed}


def load_json_record(record: dict[str, Any], label: str) -> Any:
    try:
        value = json.loads(record['stdout'])
    except json.JSONDecodeError as error:
        raise EvidenceError(f'{label} did not return JSON: {error}') from error
    return value


def fresh_query(packet: Path) -> list[dict[str, Any]]:
    jq = shutil.which('jq')
    rg = shutil.which('rg')
    if jq is None or rg is None:
        raise EvidenceError('required jq/rg executable is missing')
    records: list[dict[str, Any]] = []
    matrix = str(MATRIX)
    prior_inventory = str(SLICE / 'artifacts/cc-evidence02/nested-fields.json')
    prior_result = str(SLICE / 'artifacts/cc-evidence02/replay-result.json')
    review02 = str(SLICE / 'artifacts/cdc-review02/result.json')
    required_queries = [
        ('matrix ancillary by record', [jq, '-c', '{sourceHead,exclusions,records: [.records[] | {name, providerOnly, interfaceOnly, implicit}]}', matrix]),
        ('messageSchema complete projection', [jq, '-c', '.records[] | select(.name=="messageSchema") | {name,fields}', matrix]),
        ('convoSchema complete projection', [jq, '-c', '.records[] | select(.name=="convoSchema") | {name,fields}', matrix]),
        ('all complete projections', [jq, '-c', '[.records[] | {name,fields}]', matrix]),
        ('prior evidence02 inventory', [jq, '-c', '{sourceHead,roots,nestedExclusions,unresolved}', prior_inventory]),
        ('prior evidence02 behavior', [jq, '-c', '{readCases,gateCases,preflightCases,negativeControls,success,modelAccesses,error}', prior_result]),
        ('prior evidence02 provenance', [jq, '-c', '{sourceHead,node,compiler,sources,experimentSha256,priorHandle}', prior_result]),
        ('CDC review02 result', [jq, '-c', '.', review02]),
        ('old wrong record control', [jq, '-c', '[.records[] | select(.name=="conversationSchema") | {name,fields}]', matrix]),
        ('old wrong-level ancillary control', [jq, '-c', '{providerOnly,interfaceOnly,implicit}', matrix]),
    ]
    for title, argv in required_queries:
        record = record_then_check(packet, title, run_record(argv, PLAN))
        value = load_json_record(record, title)
        if title == 'matrix ancillary by record':
            if value.get('sourceHead') != EXPECTED_SOURCE_HEAD or [r.get('name') for r in value.get('records', [])] != ['messageSchema', 'convoSchema']:
                raise EvidenceError('correct ancillary query returned unexpected record identities')
            expected_counts = {'messageSchema': (10, 4), 'convoSchema': (13, 3)}
            for row in value['records']:
                if len(row.get('providerOnly', [])) != expected_counts[row['name']][0] or len(row.get('interfaceOnly', [])) != expected_counts[row['name']][1] or set(row.get('implicit', {})) != {'createdAt', 'updatedAt', '_id', '__v'}:
                    raise EvidenceError(f'ancillary counts or implicit keys mismatch for {row.get("name")}')
        elif title.endswith('complete projection'):
            if value.get('name') not in {'messageSchema', 'convoSchema'} or len(value.get('fields', [])) != {'messageSchema': 44, 'convoSchema': 73}[value['name']]:
                raise EvidenceError(f'{title} field count mismatch')
            if len({item['name'] for item in value['fields']}) != len(value['fields']):
                raise EvidenceError(f'{title} field identity is not unique')
        elif title == 'all complete projections':
            if [(row['name'], len(row['fields'])) for row in value] != [('messageSchema', 44), ('convoSchema', 73)]:
                raise EvidenceError('complete projection membership/count mismatch')
        elif title == 'old wrong record control' and value != []:
            raise EvidenceError('wrong record-name control unexpectedly returned data')
        elif title == 'old wrong-level ancillary control' and value != {'providerOnly': None, 'interfaceOnly': None, 'implicit': None}:
            raise EvidenceError('wrong-level ancillary control changed historical output')
    surfaces = ['api/app/clients', 'api/server/routes/messages.js', 'api/server/controllers/agents', 'packages/api/src/conversations', 'packages/api/src/agents/hitl', 'packages/data-provider/src']
    for term in ['content', 'files', 'attachments', 'metadata', 'feedback', 'contextMeta', 'userSubmittedMessageFieldPaths', 'examples', 'codeWorkspaces', 'subagentThread']:
        record = run_record([rg, '-n', '--no-heading', '-F', term, *surfaces], SOURCE)
        record_then_check(packet, f'bounded source search: {term}', record, {0, 1})
        records.append(record)
    ranges = [
        ('packages/data-provider/src/types/agents.ts', 81, 135), ('packages/data-provider/src/types/files.ts', 150, 221), ('packages/data-provider/src/types/web.ts', 19, 58), ('packages/data-provider/src/types/web.ts', 403, 420),
        ('packages/data-provider/src/types/content.ts', 1, 220), ('packages/data-provider/src/types/content.ts', 244, 315), ('packages/data-provider/src/schemas.ts', 867, 876), ('packages/data-provider/src/schemas.ts', 1039, 1061), ('packages/data-provider/src/schemas.ts', 1102, 1113), ('packages/data-provider/src/schemas.ts', 1127, 1136),
        ('packages/data-provider/src/codeEnvRef.ts', 68, 77), ('packages/data-provider/src/feedback.ts', 1, 145), ('packages/data-provider/src/filters.ts', 184, 191), ('packages/data-schemas/src/schema/message.ts', 103, 121), ('packages/data-schemas/src/schema/message.ts', 138, 151), ('packages/data-schemas/src/schema/message.ts', 238, 247), ('packages/data-schemas/src/schema/convo.ts', 35, 65), ('packages/data-schemas/src/schema/defaults.ts', 20, 40), ('packages/data-schemas/src/schema/defaults.ts', 115, 145), ('packages/data-schemas/src/schema/defaults.ts', 225, 239), ('packages/data-schemas/src/schema/defaults.ts', 320, 345), ('packages/data-schemas/src/schema/fading.ts', 1, 35),
        ('packages/data-schemas/src/types/message.ts', 47, 142), ('packages/data-schemas/src/types/convo.ts', 249, 304), ('packages/data-schemas/src/methods/message.ts', 456, 481), ('packages/data-schemas/src/methods/message.ts', 939, 975), ('packages/data-schemas/src/methods/conversation.ts', 2060, 2078), ('api/server/routes/messages.js', 67, 133), ('api/server/routes/messages.js', 232, 360), ('api/server/routes/messages.js', 565, 705), ('api/server/controllers/agents/client.js', 2249, 2320),
    ]
    for path, start, end in ranges:
        record = run_record(['sed', '-n', f'{start},{end}p', path], SOURCE)
        record_then_check(packet, f'source declaration read: {path}:{start}-{end}', record)
        records.append(record)
    historical = run_record([rg, '-n', '-C', '4', 'conversationSchema|providerOnly|self-test controls|resealed|allowedDifferences', str(SLICE / 'artifacts/cc-evidence02/execution.log')], PLAN)
    record_then_check(packet, 'historical evidence02 failure search', historical, {0, 1})
    records.append(historical)
    append_log(packet, 'fresh corrected required-data queries, negative controls, bounded searches, and source reads', records)
    return records


def harness_command(output: Path) -> list[str]:
    return [str(NODE), str(SEALED / 'experiment.cjs'), str(SOURCE), str(COMPILER), str(PRIOR / 'handle.cjs'), str(output)]


def run_capture(packet: Path) -> dict[str, Any]:
    packet_inputs(packet, sealed=False)
    inventory = read_json(packet / 'nested-fields.json')
    matrix = read_json(MATRIX)
    structural = validate_inventory(inventory, matrix)
    observed, commands = collect_environment()
    preflight = verify_environment(inventory, observed)
    append_log(packet, 'capture preflight commands and predicates', {'commands': commands, 'preflight': preflight, 'structural': structural})
    fresh_query(packet)
    result_path = packet / 'replay-result.json'
    if result_path.exists():
        append_log(packet, 'prior replay bytes preserved before capture replacement', result_path.read_text(encoding='utf-8'))
    replay = record_then_check(packet, 'pass05 replay', run_record(harness_command(result_path), PLAN))
    actual = read_json(result_path)
    baseline = read_json(SEALED_RESULT)
    submitted_comparison = exact_compare(actual, baseline, 'fresh capture versus pinned baseline')
    append_log(packet, 'exact fresh replay versus pinned baseline', submitted_comparison)
    validator = record_then_check(packet, 'sealed pass05 validator', run_record([sys.executable, str(SEALED / 'validate.py'), str(SOURCE)], PLAN))
    return {'structural': structural, 'preflight': preflight, 'replay': replay, 'comparison': submitted_comparison, 'validator': validator}


def verify_packet(packet: Path, injected_runner: Callable[[], tuple[dict[str, Any], dict[str, Any]]] | None = None, observed: dict[str, Any] | None = None) -> dict[str, Any]:
    packet_inputs(packet, sealed=True)
    before = packet_hashes(packet)
    inventory = read_json(packet / 'nested-fields.json')
    structural = validate_inventory(inventory, read_json(MATRIX))
    environment, environment_commands = collect_environment() if observed is None else (copy.deepcopy(observed), [])
    preflight = verify_environment(inventory, environment)
    submitted = read_json(packet / 'replay-result.json')
    baseline = read_json(SEALED_RESULT)
    submitted_comparison = exact_compare(submitted, baseline, 'submitted replay versus pinned baseline')
    with tempfile.TemporaryDirectory(prefix='cc-evidence03-verify-') as temporary:
        output = Path(temporary) / 'replay-result.json'
        if injected_runner is None:
            record = run_record(harness_command(output), PLAN)
            if record['exitCode'] != 0:
                raise EvidenceError('verification harness failed')
            actual = read_json(output) if output.exists() else None
        else:
            record, actual = injected_runner()
        if record['exitCode'] != 0 or actual is None:
            raise EvidenceError('verification harness produced no successful result')
        fresh_submitted = exact_compare(actual, submitted, 'fresh replay versus submitted replay')
        fresh_baseline = exact_compare(actual, baseline, 'fresh replay versus pinned baseline')
    after = packet_hashes(packet)
    if before != after:
        raise EvidenceError('packet hash changed during read-only verification')
    return {'mode': 'verify', 'packetBefore': before, 'environmentCommands': environment_commands, 'structural': structural, 'preflight': preflight, 'submittedComparison': submitted_comparison, 'harness': record, 'freshSubmittedComparison': fresh_submitted, 'freshBaselineComparison': fresh_baseline, 'packetAfter': after, 'packetUnchanged': True}


def expect_rejection(label: str, thunk: Callable[[], Any]) -> dict[str, Any]:
    try:
        thunk()
    except (EvidenceError, AssertionError) as error:
        return {'control': label, 'rejected': True, 'error': str(error)}
    return {'control': label, 'rejected': False}


def seal_copy(source_packet: Path, temporary: Path, mutation: Callable[[Path], None] | None = None) -> Path:
    temporary.mkdir(parents=True, exist_ok=True)
    for name in PACKET_FILES - {'SHA256SUMS'}:
        shutil.copy2(source_packet / name, temporary / name)
    if mutation:
        mutation(temporary)
    (temporary / 'SHA256SUMS').write_text('\n'.join(f'{digest(temporary / name)}  {name}' for name in sorted(PACKET_FILES - {'SHA256SUMS'})) + '\n', encoding='utf-8')
    return temporary


def self_test(packet: Path) -> dict[str, Any]:
    if not packet.is_dir() or not (packet / 'nested-fields.json').is_file() or not (packet / 'replay-result.json').is_file():
        raise EvidenceError('self-test requires a captured packet')
    inventory = read_json(packet / 'nested-fields.json')
    matrix = read_json(MATRIX)
    valid = validate_inventory(inventory, matrix)
    base, _ = collect_environment()
    negative: list[dict[str, Any]] = []
    positive: list[dict[str, Any]] = []
    preflight_calls = {'wrong-runtime': 0, 'wrong-head': 0, 'wrong-compiler': 0, 'wrong-source': 0}
    for label, override in [('wrong-runtime', {'node': 'v0.invalid'}), ('wrong-head', {'sourceHead': '0' * 40}), ('wrong-compiler', {'compilerSha256': '0' * 64}), ('wrong-source', {'sourceDigestOverrides': {inventory['sources'][0]['path']: '0' * 64}})]:
        def runner(label: str = label) -> tuple[dict[str, Any], dict[str, Any]]:
            preflight_calls[label] += 1
            raise AssertionError(f'{label} runner must not be called')
        negative.append(expect_rejection(f'actual-verification-path-{label}', lambda override=override, runner=runner: verify_packet(packet, injected_runner=runner, observed={**base, **override})))
    bad_classification = copy.deepcopy(inventory)
    bad_classification['coverage'][0]['classification'] = 'invalid-unclassified'
    negative.append(expect_rejection('invalid-classification', lambda: validate_inventory(bad_classification, matrix)))
    misassigned = copy.deepcopy(inventory)
    wrong_label = 'default-hidden specialized field'
    misassigned['coverage'][0]['classification'] = wrong_label
    negative.append(expect_rejection('valid-but-misassigned-classification', lambda: validate_inventory(misassigned, matrix)))
    missing = copy.deepcopy(inventory)
    missing['coverage'].pop()
    negative.append(expect_rejection('missing-field', lambda: validate_inventory(missing, matrix)))
    duplicate = copy.deepcopy(inventory)
    duplicate['coverage'].append(copy.deepcopy(duplicate['coverage'][0]))
    negative.append(expect_rejection('duplicate-field', lambda: validate_inventory(duplicate, matrix)))
    exclusion = copy.deepcopy(inventory)
    exclusion['nestedExclusions'][0]['permittedSiblings'][0]['path'] = exclusion['nestedExclusions'][0]['path']
    negative.append(expect_rejection('survivor-covered-by-exclusion', lambda: validate_inventory(exclusion, matrix)))
    sealed_result = read_json(SEALED_RESULT)
    mutation_cases = [
        ('submitted-success-false', lambda target: target.__setitem__('success', False)),
        ('submitted-node-wrong', lambda target: target.__setitem__('node', 'v0.invalid')),
        ('submitted-success-absent', lambda target: target.pop('success', None)),
        ('submitted-success-null', lambda target: target.__setitem__('success', None)),
    ]
    with tempfile.TemporaryDirectory(prefix='cc-evidence03-selftest-') as temporary:
        temporary_root = Path(temporary)
        for label, mutate_result in mutation_cases:
            def mutate(target: Path, mutate_result: Callable[[dict[str, Any]], None] = mutate_result) -> None:
                result = read_json(target / 'replay-result.json')
                mutate_result(result)
                (target / 'replay-result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
            clone = seal_copy(packet, temporary_root / label, mutate)
            negative.append(expect_rejection(label + '-through-verification-entry', lambda clone=clone: verify_packet(clone, injected_runner=lambda: ({'exitCode': 0, 'argv': ['must-not-be-called'], 'cwd': str(PLAN), 'startedAt': stamp(), 'finishedAt': stamp(), 'stdout': '', 'stderr': ''}, sealed_result))))
        unchanged = seal_copy(packet, temporary_root / 'positive-unchanged')
        before = packet_hashes(unchanged)
        valid_calls = {'count': 0}
        def valid_runner() -> tuple[dict[str, Any], dict[str, Any]]:
            valid_calls['count'] += 1
            return ({'exitCode': 0, 'argv': ['valid-sentinel'], 'cwd': str(PLAN), 'startedAt': stamp(), 'finishedAt': stamp(), 'stdout': '', 'stderr': ''}, sealed_result)
        result = verify_packet(unchanged, injected_runner=valid_runner)
        positive.append({'control': 'positive-unchanged-packet', 'rejected': False, 'packetUnchanged': result['packetUnchanged'], 'runnerCalls': valid_calls['count'], 'hashesUnchanged': before == packet_hashes(unchanged)})
        def mutate_after_hash(target: Path) -> None:
            with (target / 'report.md').open('a', encoding='utf-8') as stream:
                stream.write('\nmutation-after-initial-hashes\n')
        mutated = seal_copy(packet, temporary_root / 'negative-runner-mutation', mutate_after_hash)
        mutation_calls = {'count': 0}
        def mutating_runner() -> tuple[dict[str, Any], dict[str, Any]]:
            mutation_calls['count'] += 1
            with (mutated / 'report.md').open('a', encoding='utf-8') as stream:
                stream.write('runner mutation\n')
            return ({'exitCode': 0, 'argv': ['mutating-sentinel'], 'cwd': str(PLAN), 'startedAt': stamp(), 'finishedAt': stamp(), 'stdout': '', 'stderr': ''}, sealed_result)
        negative.append(expect_rejection('negative-runner-mutation-rejected-by-final-guard', lambda: verify_packet(mutated, injected_runner=mutating_runner)))
        positive.append({'control': 'positive-unchanged-packet-separate-from-negative-mutation', 'rejected': False, 'runnerCalls': mutation_calls['count'], 'negativeMutation': True})
        negative.append(expect_rejection('capture-refuses-sealed-destination', lambda: packet_inputs(unchanged, sealed=False)))
        sealed_before = packet_hashes(packet)
        sealed_self = self_test_sealed_read_only(packet, inventory, matrix)
        if sealed_before != packet_hashes(packet):
            raise EvidenceError('self-test mutated the sealed packet')
    failed_preflight_calls = sum(preflight_calls.values())
    if failed_preflight_calls != 0 or valid_calls['count'] != 1:
        raise EvidenceError(f'runner sentinel counts invalid: failed={failed_preflight_calls}, valid={valid_calls["count"]}')
    if not all(item.get('rejected') for item in negative):
        raise EvidenceError('one or more negative self-test controls did not reject')
    result = {'validControl': valid, 'positiveChecks': positive, 'negativeControls': negative, 'rejections': sum(item.get('rejected', False) for item in negative), 'runnerSentinel': {'failingPathCalls': failed_preflight_calls, 'validPathCalls': valid_calls['count'], 'expectedFailingPathCalls': 0, 'expectedValidPathCalls': 1}, 'sealedPacketHashPreserved': True, 'sealedReadOnlyOutput': sealed_self}
    if not (packet / 'SHA256SUMS').exists():
        append_log(packet, 'self-test controls before sealing', result)
    return result


def self_test_sealed_read_only(packet: Path, inventory: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    valid = validate_inventory(inventory, matrix)
    return {'mode': 'sealed-safe-self-test', 'validControl': valid, 'packetMutation': False, 'logMutation': False}


def main() -> int:
    parser = argparse.ArgumentParser(description='CC evidence03 capture/verify/self-test driver')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--capture', action='store_true')
    modes.add_argument('--verify', action='store_true')
    modes.add_argument('--self-test', action='store_true')
    parser.add_argument('--packet', type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args()
    if not any((args.capture, args.verify, args.self_test)):
        parser.print_usage(sys.stderr)
        return 2
    mode = 'capture' if args.capture else 'verify' if args.verify else 'self-test'
    try:
        result = run_capture(args.packet) if args.capture else verify_packet(args.packet) if args.verify else self_test(args.packet)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (EvidenceError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(json.dumps({'mode': mode, 'success': False, 'blocked': True, 'error': str(error)}, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
