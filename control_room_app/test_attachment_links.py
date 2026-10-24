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

docs = load('documents')
expenses = load('expenses')
proofs = load('proofs')

print(f"Total docs: {len(docs)}, Total expenses: {len(expenses)}, Total proofs: {len(proofs)}, Total attachments: {len(manifest)}")

# Map attachments by related_record_id and order_id
att_by_rel = {a.get('related_record_id'): a for a in manifest if a.get('related_record_id')}
att_by_order = {}
for a in manifest:
    oid = a.get('order_id')
    if oid:
        att_by_order.setdefault(oid, []).append(a)

linked_docs = 0
for d in docs:
    att = att_by_rel.get(d['id'])
    if att:
        linked_docs += 1
print(f"Linked documents with PDF file: {linked_docs} of {len(docs)}")

linked_expenses = 0
for ex in expenses:
    att = att_by_rel.get(ex['id'])
    if att:
        linked_expenses += 1
print(f"Linked expenses with receipt PDF: {linked_expenses} of {len(expenses)}")

linked_proofs = 0
for pr in proofs:
    att = att_by_rel.get(pr['id'])
    if att:
        linked_proofs += 1
print(f"Linked proofs with photo: {linked_proofs} of {len(proofs)}")
