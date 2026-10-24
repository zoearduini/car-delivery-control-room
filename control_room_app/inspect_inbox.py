import os
import json

REPO_DIR = os.path.join('.', 'car-delivery-control-room-main', 'car-delivery-control-room-main')
DATA_DIR = os.path.join(REPO_DIR, 'dataset', 'data')

def load(table):
    path = os.path.join(DATA_DIR, f'{table}.jsonl')
    out = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for l in f:
                out.append(json.loads(l))
    return out

threads = load('support_inbox_threads')
msgs = load('support_inbox_messages')
drivers = {d['id']: d for d in load('drivers')}
customers = {c['id']: c for c in load('customers')}

for i, t in enumerate(threads):
    print(f"=== Thread {i+1}: {t['id']} ===")
    cp_id = t.get('counterparty_id')
    cp_type = t.get('counterparty_type')
    cp_name = ''
    if cp_type == 'driver':
        cp_name = drivers.get(cp_id, {}).get('display_name', cp_id)
    else:
        cp_name = customers.get(cp_id, {}).get('name', cp_id)
    print(f"From: {cp_name} ({cp_type}) | Category: {t.get('category')} | Status: {t.get('status')}")
    print(f"Reason: {t.get('candidate_basis')}")
    t_m = [m for m in msgs if m.get('thread_id') == t['id']]
    for m in t_m:
        print(f"  Message: \"{m.get('body')}\"")
