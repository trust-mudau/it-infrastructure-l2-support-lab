#!/usr/bin/env python3
from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

def read_csv(name):
    with (DATA / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

assets = read_csv('assets.csv')
tickets = read_csv('tickets.csv')
reviews = read_csv('access_review.csv')

required_asset = ['asset_id','asset_type','make_model','serial','status','location']
asset_errors=[]
seen=set()
for row in assets:
    missing=[k for k in required_asset if not row.get(k,'').strip()]
    if missing: asset_errors.append(f"{row.get('asset_id','UNKNOWN')}: missing {','.join(missing)}")
    if row['asset_id'] in seen: asset_errors.append(f"duplicate asset_id {row['asset_id']}")
    seen.add(row['asset_id'])
    if row['status']=='Assigned' and not row.get('user','').strip():
        asset_errors.append(f"{row['asset_id']}: assigned asset has no user")

sla_results=[]
for row in tickets:
    start=datetime.fromisoformat(row['created_at'])
    end=datetime.fromisoformat(row['resolved_at'])
    elapsed=(end-start).total_seconds()/3600
    target=float(row['sla_hours'])
    met=elapsed <= target
    sla_results.append((row['ticket_id'], elapsed, target, met, row['status'], row['escalation']))

review_errors=[]
for row in reviews:
    if row['decision']=='Remove' and row['action_status']!='Completed':
        review_errors.append(f"{row['review_id']}: removal not completed")
    if row['decision']=='Keep' and row['action_status'] not in {'Verified','Completed'}:
        review_errors.append(f"{row['review_id']}: keep decision not verified")

met_count=sum(1 for x in sla_results if x[3])
sla_pct=(met_count/len(sla_results))*100 if sla_results else 0

lines=[
'# GreenCo-aligned Mini-Pack Validation Report','',
'Generated from synthetic portfolio data. This report does not represent GreenCo production systems.','',
'## Summary','',
f'- Assets checked: {len(assets)}',
f'- Asset validation errors: {len(asset_errors)}',
f'- Tickets checked: {len(tickets)}',
f'- Tickets meeting synthetic SLA: {met_count}/{len(tickets)} ({sla_pct:.1f}%)',
f'- Access-review rows checked: {len(reviews)}',
f'- Access-review validation errors: {len(review_errors)}','',
'## Ticket SLA detail','',
'| Ticket | Elapsed h | Target h | SLA met | Status | Escalated |','|---|---:|---:|---|---|---|'
]
for tid,elapsed,target,met,status,esc in sla_results:
    lines.append(f'| {tid} | {elapsed:.2f} | {target:.0f} | {"YES" if met else "NO"} | {status} | {esc} |')
lines += ['', '## Asset validation', '']
lines += [f'- {e}' for e in asset_errors] if asset_errors else ['- PASS: required asset fields and assignment checks passed.']
lines += ['', '## Access review validation', '']
lines += [f'- {e}' for e in review_errors] if review_errors else ['- PASS: removal decisions are completed and keep decisions are verified.']
lines += ['', '## Result', '']
if asset_errors or review_errors or met_count != len(sla_results):
    lines.append('**FAILED** - one or more validation checks require correction.')
    result=1
else:
    lines.append('**PASS** - synthetic asset, SLA and access-review records passed validation.')
    result=0

out='\n'.join(lines)+'\n'
(REPORTS/'validation-report.md').write_text(out, encoding='utf-8')
print(out)
raise SystemExit(result)
