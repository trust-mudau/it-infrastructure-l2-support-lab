import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / 'ticket_queue.csv'
TICKETS_MD = ROOT / 'tickets.md'

required_categories = {
    'Password reset', 'Locked account', 'Access issue', 'Software failure',
    'Hardware peripheral', 'Networking connectivity', 'Phishing security',
    'Application failure', 'Printer peripheral', 'Onboarding access'
}
allowed_priorities = {'P1', 'P2', 'P3', 'P4'}
allowed_statuses = {'New', 'Open', 'Pending', 'Resolved', 'Closed', 'Escalated'}

with CSV_PATH.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

assert len(rows) == 10, f'Expected 10 tickets, found {len(rows)}'
ids = [r['ticket_id'] for r in rows]
assert len(ids) == len(set(ids)), 'Duplicate ticket IDs found'
assert required_categories == {r['category'] for r in rows}, 'Ticket category coverage incomplete'
assert all(r['priority'] in allowed_priorities for r in rows), 'Invalid priority found'
assert all(r['status'] in allowed_statuses for r in rows), 'Invalid status found'
assert all(int(r['sla_hours']) > 0 for r in rows), 'SLA hours must be positive'

escalated = [r for r in rows if r['status'] == 'Escalated']
assert len(escalated) >= 2, 'Expected at least two escalation cases'
assert all(r['escalation_target'] != 'None' for r in escalated), 'Escalated ticket missing target'

md = TICKETS_MD.read_text(encoding='utf-8')
required_fields = [
    '**Issue:**', '**Priority:**', '**Diagnostic Questions:**', '**Troubleshooting:**',
    '**Resolution/Escalation:**', '**User Communication:**', '**Closure Notes:**'
]
for ticket_id in ids:
    assert ticket_id in md, f'{ticket_id} missing from ticket documentation'
for field in required_fields:
    assert md.count(field) >= 10, f'Field {field} is not present for all tickets'

resolved = sum(r['status'] == 'Resolved' for r in rows)
print(f'Validated {len(rows)} helpdesk tickets')
print(f'Resolved at L1: {resolved}')
print(f'Escalated: {len(escalated)}')
print('Ticket workflow validation: PASS')
