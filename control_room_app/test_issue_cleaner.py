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

alerts = load('alerts')
incidents = load('incidents')
proposals = load('agent_proposals')
claims = load('endpoint_claims')
work_items = load('work_items')
orders = load('orders')

def get_issue_info(order_id):
    incs = [i for i in incidents if i.get('order_id') == order_id and not i.get('resolved_at')]
    als = [a for a in alerts if a.get('order_id') == order_id and a.get('status') == 'OPEN']
    props = [p for p in proposals if p.get('order_id') == order_id and p.get('status') == 'PENDING_REVIEW']
    clms = [c for c in claims if c.get('order_id') == order_id and c.get('resolution_status') == 'OPEN']
    wis = [w for w in work_items if w.get('order_id') == order_id and w.get('status') == 'OPEN']

    if not (incs or als or props or clms or wis):
        return {"short_title": "On Track", "full_description": "Vehicle operations proceeding on schedule without manual intervention."}

    full_desc = ""
    short_title = ""

    # Incidents take highest priority
    for inc in incs:
        kind = inc.get("kind", "")
        symp = inc.get("reported_symptom") or inc.get("reported_stop_text")
        if kind == "VEHICLE_WARNING":
            short_title = "Engine Warning Light"
            full_desc = symp or "Vehicle reported dashboard warning light; vehicle safely halted en route."
            break
        elif kind == "TRAVEL_CAPACITY":
            short_title = "Ferry Sold Out"
            full_desc = symp or "Scheduled ferry departure sold out; maritime booking re-accommodation required."
            break
        elif kind == "EMPTY_PICKUP":
            short_title = "Pickup Site Refusal"
            full_desc = symp or "Origin site refused handover or vehicle unavailable upon driver arrival."
            break
        elif kind == "POST_DELIVERY_CONDITION_CLAIM":
            short_title = "Damage Claim Reported"
            full_desc = symp or "Buyer filed post-delivery cosmetic condition claim."
            break
        elif symp:
            short_title = "Operational Incident"
            full_desc = symp
            break

    if not short_title:
        for cl in clms:
            short_title = "Damage Claim Filed"
            full_desc = cl.get("claim_text") or cl.get("summary") or "Post-delivery cosmetic condition claim requires operator verification."
            break

    if not short_title:
        for wi in wis:
            summary = wi.get("summary", "")
            full_desc = summary
            lower = summary.lower()
            if "hold" in lower or "release" in lower or "seller" in lower:
                short_title = "Missing Seller Release"
            elif "access" in lower or "receiver" in lower or "authorized" in lower:
                short_title = "Receiver Authority Missing"
            elif "ferry" in lower or "sailing" in lower:
                short_title = "Ferry Rebooking Required"
            elif "expense" in lower or "receipt" in lower or "parking" in lower:
                short_title = "Expense Receipt Missing"
            elif "warning" in lower or "recovery" in lower:
                short_title = "Vehicle Warning Review"
            elif "driver" in lower:
                short_title = "Driver Duty Conflict"
            else:
                short_title = "Dispatch Action Required"
            break

    if not short_title:
        for pr in props:
            summary = pr.get("summary", "")
            full_desc = summary
            lower = summary.lower()
            if "ferry" in lower or "crossing" in lower or "travel" in lower:
                short_title = "Ferry Booking Review"
            elif "release" in lower or "document" in lower:
                short_title = "Document Verification"
            else:
                short_title = "Proposal Pending Review"
            break

    if not short_title:
        for al in als:
            summary = al.get("summary", "")
            full_desc = summary
            lower = summary.lower()
            if "tracking" in lower or "gap" in lower:
                short_title = "Tracking Signal Lost"
            elif "release" in lower or "document" in lower:
                short_title = "Document Hold Alert"
            elif "access" in lower:
                short_title = "Delivery Access Alert"
            else:
                short_title = "Operational Alert"
            break

    return {"short_title": short_title or "Needs Review", "full_description": full_desc or "Operational issue requires dispatcher review."}

issues = []
for o in orders:
    info = get_issue_info(o['id'])
    if info['short_title'] != 'On Track':
        issues.append((o['id'], o.get('reference'), info['short_title'], info['full_description']))

print(f"Total issue orders: {len(issues)}")
for oid, ref, short_t, full_d in issues:
    print(f"{ref} ({oid}) -> SHORT: [{short_t}] | FULL: {full_d[:70]}...")
