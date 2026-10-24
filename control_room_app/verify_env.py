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

print("Data loaded successfully.")
