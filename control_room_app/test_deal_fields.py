import os
import json

REPO_DIR = os.path.join('.', 'car-delivery-control-room-main', 'car-delivery-control-room-main')
DATA_DIR = os.path.join(REPO_DIR, 'dataset', 'data')
ATTACHMENTS_DIR = os.path.join(REPO_DIR, 'attachments')

def load(table):
    path = os.path.join(DATA_DIR, f'{table}.jsonl')
    out = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for l in f:
                out.append(json.loads(l))
    return out

manifest = []
m_path = os.path.join(ATTACHMENTS_DIR, 'manifest.json')
if os.path.exists(m_path):
    with open(m_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

att_by_rel = {a.get('related_record_id'): a for a in manifest if a.get('related_record_id')}
items = load('order_items')
windows = load('time_windows')
print("Sample order_item:", items[0] if items else "none")
print("Sample time_window:", windows[0] if windows else "none")
