#!/usr/bin/env python3
"""Replay pass05 and validate the CC evidence packet's structural claims."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PLAN = Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning')
SOURCE = Path('/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall')
SLICE = PLAN / 'project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design'
OUT = SLICE / 'artifacts/cc-evidence01'
SEALED = SLICE / 'artifacts/design-pass05'
PRIOR = SLICE / 'artifacts/design-pass04'
NODE = Path('/Users/oubiwann/.local/bin/node')
COMPILER = Path('/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js')
MATRIX = SEALED / 'field-matrix.json'
SEALED_RESULT = SEALED / 'result-01.json'
LOG = OUT / 'execution.log'

ROOTS = {
    'message': {'content', 'files', 'attachments', 'metadata', 'feedback', 'contextMeta', 'userSubmittedMessageFieldPaths'},
    'conversation': {'examples', 'codeWorkspaces', 'subagentThread'},
}
NESTED_EXCLUSIONS = {
    'metadata.thoughtSignatures',
    'content.tool_call.backgroundTask.resultClaim',
    'content.tool_call.backgroundTask.completionWakeup',
    'attachments.web_search.knowledgeGraph',
    'attachments.web_search.peopleAlsoAsk',
    'attachments.web_search.relatedSearches',
    'attachments.web_search.shopping',
    'attachments.web_search.places',
    'attachments.web_search.news',
    'attachments.web_search.organic.sitelinks',
    'attachments.web_search.organic.highlights',
    'attachments.web_search.topStories.highlights',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(title: str, value: object) -> None:
    with LOG.open('a', encoding='utf-8') as stream:
        stream.write(f'\n[{stamp()}] {title}\n')
        stream.write(json.dumps(value, indent=2) if not isinstance(value, str) else value)
        stream.write('\n')


def command(title: str, argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    started = stamp()
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    log(title, {
        'argv': argv,
        'cwd': str(cwd),
        'startedAt': started,
        'finishedAt': stamp(),
        'exitCode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
    })
    return result


def classification(record: str, field: str) -> str:
    if field in ROOTS[record]:
        return 'selected nested root'
    if record == 'conversation' and field == 'messages':
        return 'adapter-private physical relationship'
    hidden = {
        'message': {'_meiliIndex', 'subagentTranscript', 'subagentActivityProjection', 'subagentTriggerProjection', 'subagentTask'},
        'conversation': {'initial_agent_id', 'subagentThreadLease', 'agentEventBinding', 'agentEventActor', 'agentEventActorCleanup', 'agentEventActorReconciliations', 'agentEventActorEpoch', 'agentEventActorLegacyTurn', 'agentEventActorSuspension'},
    }
    if field in hidden[record]:
        return 'default-hidden specialized field'
    return 'other scalar/array field outside this deep inspection'


def root(record: str, field: str, schema: str, server: str, provider: str, nested: str, state: str, witnesses: list[str], evidence: str) -> dict:
    return {
        'record': record,
        'field': field,
        'schema': schema,
        'directType': {'server': server, 'provider': provider},
        'nestedShape': nested,
        'applicability': 'Server history/public or settings use is recorded from the cited source; the ordinary access probe carries no full value for this root unless stated otherwise.',
        'fieldStateAndUnset': state,
        'witnesses': witnesses,
        'evidenceClass': evidence,
        'owner': 'CDC for unresolved codec/DTO policy',
    }


def make_roots() -> list[dict]:
    return [
        root('message', 'content', 'message.ts:139-143; Mixed[]; default undefined; implicit member id not established', 'IMessage.content?: unknown[] (types/message.ts:90)', 'TMessage.content?: TMessageContentParts[] (schemas.ts:1063-1066)', 'Array boundary content[index]; ContentTypes discriminants and union members at types/content.ts:244-315; tool-call and provider fallback retain open/object values.', 'Absent, null, empty and populated are distinct; nested exclusions remove two background-task paths while preserving siblings.', ['routes/messages.js:243-360 branch projection and :582-691 structured text edit', 'methods/message.ts:258-269 provenance path and :1182-1410 tool/attachment patch'], 'schema/type/witness; no historical BSON characterization'),
        root('message', 'files', 'message.ts:138; Mixed[]; default undefined; implicit member id not established', 'IMessage.files?: unknown[] (types/message.ts:83)', 'TMessage.files?: Partial<TFile>[] (schemas.ts:1063-1069)', 'Array of open storage values; provider Partial<TFile> is a shallow consumer type (types/files.ts:150-221), not a lossless decoder.', 'Absent, null, empty and populated are distinct; null acceptance and codec are unresolved.', ['BaseClient and formatMessages consume file references in the bounded search surface', 'types/files.ts:150-221 declares the provider shape'], 'schema/consumer type; no historical value characterization'),
        root('message', 'attachments', 'message.ts:247; Mixed[]; default undefined; implicit member id not established', 'IMessage.attachments?: unknown[] (types/message.ts:126)', 'TMessage.attachments?: TAttachment[] (schemas.ts:1063-1069)', 'Array of TAttachment union branches (schemas.ts:1039-1061) with TFile plus message/tool/resource metadata; nine web-search nested paths are excluded publicly.', 'Absent, null, empty and populated are distinct; preserve array and permitted siblings.', ['routes/messages.js:322-346 branch copies attachments', 'methods/message.ts:1182-1410 merges attachments; CLIENT_MESSAGE_SELECT:472-480 excludes exact paths'], 'schema/provider union/witness; no database characterization'),
        root('message', 'metadata', 'message.ts:151; Mixed; default/required not declared', 'IMessage.metadata?: Record<string, unknown> (types/message.ts:94)', 'tMessageSchema.metadata: z.record(z.unknown()).optional() (schemas.ts:928-929)', 'No closed member vocabulary; arbitrary record values may nest arrays/objects and storage may contain non-JSON BSON.', 'Absent, null, empty object and populated object are distinct; thoughtSignatures is excluded from public reads.', ['CLIENT_MESSAGE_SELECT:469 excludes metadata.thoughtSignatures', 'bounded ordinary-path search found many unrelated metadata namespaces'], 'Mixed schema/record type; semantic vocabulary unresolved'),
        root('message', 'feedback', 'message.ts:103-121; object rating enum, tag Mixed optional, text string optional; default undefined', 'IMessage.feedback with TFeedbackTag|undefined (types/message.ts:73-77)', 'feedbackSchema/TFeedback (feedback.ts:110-133), used by tMessageSchema at schemas.ts:927', 'No array; stored tag is Mixed, provider minimal schema requires a tag key and validates rating direction, while TFeedback exposes an expanded tag object.', 'Absent, null, empty and populated differ; provider/server tag representation needs CDC policy.', ['routes/messages.js:693-705 begins feedback validation', 'feedback.ts:110-145 validates and converts minimal/expanded forms'], 'schema/provider mismatch/witness; stored tag history unknown'),
        root('message', 'contextMeta', 'message.ts:238-246; object with _id:false, default undefined, plus fading spread', 'IMessage.contextMeta?: Partial<IAgentEventActorContextMeta> (types/message.ts:125)', 'tMessageSchema.contextMeta (schemas.ts:932-956)', 'fading.ts:19-34 expands fading {v,budgetTokens,masked} and fadingTiers[{agentId,...}]; no open member in selected declarations.', 'Absent/null/populated differ; explicit null unsets on save (methods/message.ts:939-945); root is public-excluded but server-retained.', ['routes/messages.js:232-241 and :332-334 client/server projection and branch carry', 'agents/client.js:2249-2267 normalize/publish and :2271-2320 retain history rows'], 'schema/local/provider types and server witnesses'),
        root('message', 'userSubmittedMessageFieldPaths', 'message.ts:74-87; _id:false array {path,field}; default undefined', 'UserSubmittedMessageFieldPath[] (types/message.ts:68)', 'filters.ts:58-62 and :184-191; tMessageSchema use at schemas.ts:906', 'Array members have required path and closed field enum answer/decision_response/decision_reason; target values remain outside this type.', 'Absent, empty and populated differ; null is not declared; path remapping must preserve content indices.', ['methods/message.ts:304-374 and :954-975 merge/normalize with CAS', 'routes/messages.js:278-345 remaps branch paths'], 'schema/provider/witness; target Mixed values unresolved'),
        root('conversation', 'examples', 'defaults.ts:30-35 and :238-239; Mixed[]; default undefined; member id not explicitly disabled', 'IConversation.examples?: unknown[] (types/convo.ts:261)', 'tExampleSchema (schemas.ts:867-876), tConversationSchema use at :1167', 'Array elements are intended input/output objects with content strings in provider schema; storage remains Mixed.', 'Absent/null/empty/populated differ; no default conversion.', ['data-provider/src/generate.ts:677-704 reads/supplies provider defaults', 'no non-test ordinary BaseClient writer for exact field was established'], 'schema/provider type; ordinary persistence producer not established'),
        root('conversation', 'codeWorkspaces', 'defaults.ts:128-135 and :327-336; _id:false array of required environmentId/workspaceId strings', 'IConversation.codeWorkspaces?: CodeWorkspaceSelection[] (types/convo.ts:285)', 'tConversationSchema.codeWorkspaces (schemas.ts:1127-1136)', 'Array boundary; provider object is strict and regex-constrained by CODE_WORKSPACE_ID_PATTERN; no open/Mixed position.', 'Absent versus empty versus populated changes agent code behavior; null policy is not declared.', ['agents/request.js:1514-1516 and :1951 resolve/pass selections', 'agents/resume.js:1812 and client.js:4561-4563 consume request/resolved values', 'api/src/agents/hitl/policy.ts:787-814 preserves presence/null'], 'schema/aligned provider type/agent witnesses; adapter conformance open'),
        root('conversation', 'subagentThread', 'convo.ts:52-65; _id:false object with required lineage IDs, kind enum and depth>=1', 'IConversation.subagentThread?: TSubagentThreadLineage (types/convo.ts:288)', 'subagentThreadLineageSchema/TSubagentThreadLineage (schemas.ts:1102-1113), use at :1203', 'No array/open position; lineage fields are nonempty strings, subagentKind is agent|graph and depth is positive integer. Lease/event-actor fields are separate hidden fields.', 'Absent versus populated controls child identity; null is not declared.', ['routes/messages.js:133 rejects public child conversations', 'agents/request.js:1737, resume.js:1326 and responses.js:708 inspect lineage'], 'schema/provider/witness; private lifecycle remains separate'),
    ]


def build_inventory(matrix: dict) -> dict:
    coverage = []
    for record in matrix['records']:
        namespace = 'message' if record['name'] == 'messageSchema' else 'conversation'
        for field in record['fields']:
            coverage.append({
                'record': namespace,
                'field': field['name'],
                'classification': classification(namespace, field['name']),
                'source': field['source'],
                'storageDefinition': field['storageDefinition'],
                'interfaceType': field['interfaceType'],
                'provider': field['provider'],
                'defaultRead': field['defaultRead'],
                'publicRead': field['publicRead'],
                'portableServerRead': field['portableServerRead'],
                'endpointUnsetRule': field['endpointUnsetRule'],
            })
    source_paths = sorted({
        'packages/data-schemas/src/schema/message.ts', 'packages/data-schemas/src/schema/convo.ts',
        'packages/data-schemas/src/schema/defaults.ts', 'packages/data-schemas/src/schema/fading.ts',
        'packages/data-schemas/src/types/message.ts', 'packages/data-schemas/src/types/convo.ts',
        'packages/data-schemas/src/methods/message.ts', 'packages/data-provider/src/schemas.ts',
        'packages/data-provider/src/feedback.ts', 'packages/data-provider/src/filters.ts',
        'packages/data-provider/src/types/content.ts', 'packages/data-provider/src/types/files.ts',
        'packages/data-provider/src/types/agents.ts', 'packages/data-provider/src/types/runs.ts',
        'api/server/routes/messages.js', 'api/server/controllers/agents/client.js',
        'api/server/controllers/agents/request.js', 'api/server/controllers/agents/resume.js',
        'api/server/controllers/agents/responses.js', 'packages/api/src/agents/hitl/answers.ts',
        'packages/api/src/agents/hitl/policy.ts', 'packages/data-provider/src/generate.ts',
        'packages/data-provider/src/data-service.ts',
    })
    unresolved = [{
        'question': question,
        'evidence': evidence,
        'affectedRoot': field,
        'owner': 'CDC',
    } for field, question, evidence in [
        ('content', 'Which portable representation preserves Mixed content and its open provider variants?', 'Mixed schema plus unknown[] and a union with open fallbacks; no historical values inspected.'),
        ('files', 'Should file references use a lossless storage shape or the shallow provider Partial<TFile>?', 'Storage is Mixed/unknown[] while the provider supplies a consumer shape.'),
        ('attachments', 'Which attachment union and nested resource values are portable?', 'TAttachment is a provider union over Mixed storage; historical values are unknown.'),
        ('metadata', 'What values and nested vocabulary must a portable metadata codec preserve?', 'Record<string, unknown> and Mixed do not establish a vocabulary.'),
        ('feedback', 'How should Mixed/expanded feedback tags map to the provider minimal key form?', 'Server and provider declarations disagree on tag representation.'),
        ('contextMeta', 'Should the DTO retain server Partial optionality or provider validation semantics?', 'Both are similar but differ in optionality and public visibility.'),
        ('userSubmittedMessageFieldPaths', 'How should path targets inside Mixed content/attachments be represented?', 'The path/field marker is closed but target values are not.'),
        ('examples', 'Can historical Mixed examples be decoded as provider input/output pairs?', 'Provider schema is narrower than storage and no ordinary producer was established.'),
        ('codeWorkspaces', 'What conformance cases cover absent/empty/populated workspace selections?', 'Declarations align but policy paths distinguish presence and null.'),
        ('subagentThread', 'How must lineage remain separate from lease/event-actor private state?', 'Source has separate fields and the ordinary probe returns only a discriminator.'),
    ]]
    return {
        'sourceHead': matrix['sourceHead'],
        'sources': [{'path': path, 'sha256': digest(SOURCE / path)} for path in source_paths],
        'coverage': coverage,
        'roots': make_roots(),
        'nestedExclusions': [{'path': path, 'source': 'packages/data-schemas/src/methods/message.ts:469-480', 'preserve': 'array structure and all permitted sibling data'} for path in sorted(NESTED_EXCLUSIONS)],
        'unresolved': unresolved,
        'limits': ['Structural replay and declarations do not choose codecs, stringify BSON, reject old records, flatten arrays or add defaults.', 'Provider/UI schemas are consumer evidence, not automatically lossless persistence decoders.', 'No Mongo access, application suite, build, migration or source edit was authorized.'],
    }


def validate_inventory(inventory: dict, matrix: dict) -> dict:
    keys = [(row['record'], row['field']) for row in inventory['coverage']]
    expected = [(('message' if record['name'] == 'messageSchema' else 'conversation'), field['name']) for record in matrix['records'] for field in record['fields']]
    assert len(keys) == 117 and len(set(keys)) == 117 and set(keys) == set(expected)
    actual_roots = {(item['record'], item['field']) for item in inventory['roots']}
    assert actual_roots == {(record, field) for record, fields in ROOTS.items() for field in fields}
    assert len(inventory['roots']) == 10
    assert {item['path'] for item in inventory['nestedExclusions']} == NESTED_EXCLUSIONS
    assert len(inventory['nestedExclusions']) == 12
    assert all(item['owner'] == 'CDC' for item in inventory['unresolved'])
    labels = ['selected nested root', 'other scalar/array field outside this deep inspection', 'default-hidden specialized field', 'adapter-private physical relationship']
    return {'coverageRows': len(keys), 'uniqueCoverageKeys': len(set(keys)), 'selectedRoots': len(inventory['roots']), 'nestedExclusions': len(inventory['nestedExclusions']), 'classificationCounts': {label: sum(row['classification'] == label for row in inventory['coverage']) for label in labels}}


def compare_results(actual: dict, sealed: dict) -> dict:
    exact = ['readCases', 'gateCases', 'preflightCases', 'negativeControls', 'success', 'modelAccesses', 'error']
    for field in exact:
        assert actual.get(field) == sealed.get(field), f'behavior mismatch: {field}'
    provenance = ['sourceHead', 'node', 'compiler', 'sources', 'experimentSha256', 'priorHandle']
    differences = [{'field': field, 'sealed': sealed.get(field), 'replay': actual.get(field)} for field in provenance if actual.get(field) != sealed.get(field)]
    return {'behaviorFieldsComparedExactly': exact, 'provenanceFieldsComparedIndividually': provenance, 'allowedProvenanceDifferences': differences}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text('# CC evidence01 execution log\nAppend-only command attempts and structural checks.\n', encoding='utf-8')
    matrix = json.loads(MATRIX.read_text(encoding='utf-8'))
    inventory = build_inventory(matrix)
    inventory_check = validate_inventory(inventory, matrix)
    (OUT / 'nested-fields.json').write_text(json.dumps(inventory, indent=2) + '\n', encoding='utf-8')
    log('inventory structural checks', inventory_check)
    replay = OUT / 'replay-result.json'
    argv = [str(NODE), str(SEALED / 'experiment.cjs'), str(SOURCE), str(COMPILER), str(PRIOR / 'handle.cjs'), str(replay)]
    run = command('pass05 replay', argv, PLAN)
    if run.returncode != 0:
        if replay.exists():
            log('failed replay result before any retry', replay.read_text(encoding='utf-8'))
        raise SystemExit(f'replay failed with exit {run.returncode}')
    comparison = compare_results(json.loads(replay.read_text(encoding='utf-8')), json.loads(SEALED_RESULT.read_text(encoding='utf-8')))
    log('replay comparison', comparison)
    validator = command('sealed pass05 validator', [sys.executable, str(SEALED / 'validate.py'), str(SOURCE)], PLAN)
    if validator.returncode != 0:
        raise SystemExit(f'sealed validator failed with exit {validator.returncode}')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip()
    status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=SOURCE, text=True)
    assert head == matrix['sourceHead'] and status == ''
    log('source preservation check', {'head': head, 'status': status, 'clean': True})
    print(json.dumps({'inventory': inventory_check, 'replay': comparison, 'validatorExit': validator.returncode}, indent=2))


if __name__ == '__main__':
    main()
