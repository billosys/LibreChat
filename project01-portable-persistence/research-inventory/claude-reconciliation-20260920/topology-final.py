"""Source-only shape/fidelity checks. Emits counts and array locators, no text."""
import collections
import datetime
import json
from pathlib import Path

source = Path('/Users/oubiwann/lab/oxur/ixy/workbench/conversations.json')
data = json.loads(source.read_text())
# Observed common external-root marker, absent from every conversation's message IDs.
root_markers = {None, '', '00000000-0000-0000-0000-000000000000',
                '00000000-0000-4000-8000-000000000000'}
stats = collections.Counter()
locators = []
for ci, conversation in enumerate(data):
    messages = conversation['chat_messages']
    by_id = {m['uuid']: m for m in messages}
    assert len(by_id) == len(messages), f'Duplicate source message IDs at {ci}'
    assert not set(by_id).intersection(root_markers)
    retained = []
    for mi, message in enumerate(messages):
        text = ''.join(p['text'] for p in message['content']
                       if p.get('type') == 'text' and p.get('text')) or message.get('text', '')
        thinking = ''.join(p['thinking'] for p in message['content']
                           if p.get('type') == 'thinking' and p.get('thinking'))
        if text or thinking:
            retained.append((mi, message))
        else:
            stats['skipped_messages'] += 1
            stats['skipped_with_any_file_or_attachment_metadata'] += bool(message.get('attachments') or message.get('files'))
    retained_ids = {m['uuid'] for _, m in retained}
    child_counts = collections.Counter(m.get('parent_message_uuid') for m in messages
                                      if m.get('parent_message_uuid') in by_id)
    branch_points = sum(n > 1 for n in child_counts.values())
    stats['branch_points'] += branch_points
    stats['conversations_with_branch_points'] += bool(branch_points)
    stats['nonempty_conversation_summaries'] += bool(conversation.get('summary'))
    stats['conversation_updated_at_differs_from_created_at'] += conversation.get('updated_at') != conversation.get('created_at')
    changed = 0
    previous = None
    for mi, message in retained:
        parent = message.get('parent_message_uuid')
        traversed = set()
        while parent in by_id and parent not in retained_ids:
            assert parent not in traversed, f'Parent cycle at {ci}/{mi}'
            traversed.add(parent)
            parent = by_id[parent].get('parent_message_uuid')
        if parent in root_markers:
            parent = None
        elif parent not in by_id:
            stats['unresolved_source_parents'] += 1
        if traversed:
            stats['retained_messages_with_skipped_ancestors'] += 1
        if parent != previous:
            changed += 1
            locators.append({'sourceConversationIndex': ci, 'sourceMessageIndex': mi,
                             'kind': 'source_parent_differs_from_linear_import'})
        previous = message['uuid']
        created = datetime.datetime.fromisoformat(message['created_at'].replace('Z', '+00:00'))
        stats['retained_timestamp_precision_below_ms'] += created.microsecond % 1000 != 0
        stats['retained_message_updated_at_differs_from_created_at'] += message.get('updated_at') != message.get('created_at')
    stats['retained_parent_relationships_changed'] += changed
    stats['conversations_with_parent_relationships_changed'] += bool(changed)

report = {
    'method': 'Source-only graph analysis; independently implement text/thinking skip predicate, normalize observed external-root marker, contract skipped ancestors, compare source parent with previous retained message. Mongo parent chains were checked separately against that sequence.',
    'counts': dict(stats),
}
Path('/tmp/guildhall-source-topology-v2.json').write_text(json.dumps(report, indent=2) + '\n')
Path('/tmp/guildhall-source-topology-locators-v2.json').write_text(json.dumps(locators, indent=2) + '\n')
print(json.dumps(report, indent=2))
