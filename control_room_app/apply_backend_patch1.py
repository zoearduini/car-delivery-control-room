import re

backend_path = "control_room_app/backend.py"

with open(backend_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update get_clean_issue_description and add get_clean_issue_info
old_issue_func = """def get_clean_issue_description(incidents, alerts, proposals, claims, work_items) -> str:
    for inc in incidents:
        symp = inc.get("reported_symptom") or inc.get("reported_stop_text")
        if symp:
            return symp
        kind = inc.get("kind", "")
        if kind == "TRAVEL_CAPACITY":
            return "Ferry departure sold out; sailing rebooking required"
        if kind == "VEHICLE_WARNING":
            return "Red dashboard warning; driver halted safely"
        if kind == "EMPTY_PICKUP":
            return "Pickup site closed or vehicle unavailable on arrival"
        if kind == "POST_DELIVERY_CONDITION_CLAIM":
            return "Post-delivery cosmetic condition claim reported"

    for wi in work_items:
        if wi.get("summary"):
            return wi["summary"]

    for al in alerts:
        if al.get("summary"):
            return al["summary"]

    for pr in proposals:
        if pr.get("summary"):
            return pr["summary"]

    for cl in claims:
        return cl.get("claim_text") or cl.get("summary") or "Post-delivery condition claim recorded"

    return "On track  -  automated operations active\""""

new_issue_func = """def get_clean_issue_info(incidents, alerts, proposals, claims, work_items) -> Dict[str, str]:
    \"\"\"
    Returns both a crisp short_title (2-4 words) for overview badges,
    and the full detailed description for car detail views.
    \"\"\"
    short_title = ""
    full_desc = ""

    # 1. Incidents (Highest Priority)
    for inc in incidents:
        kind = inc.get("kind", "")
        symp = inc.get("reported_symptom") or inc.get("reported_stop_text")
        if kind == "VEHICLE_WARNING":
            short_title = "Engine Warning Light"
            full_desc = symp or "Vehicle reported red dashboard warning and reduced acceleration; driver halted safely."
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

    # 2. Claims
    if not short_title:
        for cl in claims:
            short_title = "Damage Claim Filed"
            full_desc = cl.get("claim_text") or cl.get("summary") or "Post-delivery cosmetic condition claim requires operator verification."
            break

    # 3. Work items
    if not short_title:
        for wi in work_items:
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
            elif "driver" in lower or "duty" in lower:
                short_title = "Driver Duty Conflict"
            elif "vin" in lower or "plate" in lower or "registration" in lower:
                short_title = "Missing VIN / Plate"
            elif "contact" in lower:
                short_title = "Missing Site Contact"
            elif "photo" in lower or "proof" in lower:
                short_title = "Inspection Photo Issue"
            elif "handover" in lower or "signature" in lower:
                short_title = "Missing Handover Record"
            elif "address" in lower:
                short_title = "Incomplete Address"
            elif "window" in lower or "deadline" in lower:
                short_title = "Delivery Window Risk"
            else:
                short_title = "Dispatch Action Required"
            break

    # 4. Proposals
    if not short_title:
        for pr in proposals:
            summary = pr.get("summary", "")
            full_desc = summary
            lower = summary.lower()
            if "ferry" in lower or "crossing" in lower or "travel" in lower:
                short_title = "Ferry Booking Review"
            elif "release" in lower or "document" in lower:
                short_title = "Document Verification"
            elif "photo" in lower or "damage" in lower:
                short_title = "Photo Inspection Review"
            else:
                short_title = "Proposal Pending Review"
            break

    # 5. Alerts
    if not short_title:
        for al in alerts:
            summary = al.get("summary", "")
            full_desc = summary
            lower = summary.lower()
            if "tracking" in lower or "gap" in lower:
                short_title = "Tracking Signal Lost"
            elif "release" in lower or "document" in lower:
                short_title = "Document Hold Alert"
            elif "access" in lower:
                short_title = "Delivery Access Alert"
            elif "ferry" in lower or "cutoff" in lower:
                short_title = "Ferry Cutoff Alert"
            elif "invoice" in lower:
                short_title = "Invoice Query Pending"
            else:
                short_title = "Operational Alert"
            break

    if not short_title:
        short_title = "On Track"
        full_desc = "On track - automated operations active"

    return {
        "short_title": short_title,
        "full_description": full_desc
    }

def get_clean_issue_description(incidents, alerts, proposals, claims, work_items) -> str:
    info = get_clean_issue_info(incidents, alerts, proposals, claims, work_items)
    return info["short_title"]"""

assert "def get_clean_issue_description" in content
content = content.replace(old_issue_func, new_issue_func)

# 2. Update get_order_attention return dictionary
old_attention = """    headline = get_clean_issue_description(incidents, alerts, proposals, claims, open_work_items) if needs_human else "On track  -  automated operations active"

    # Pre-flight real checklist derived from actual data
    order_tracks = [t for t in DATA.get("tracking_observations", []) if t.get("order_id") == order_id]
    order_res = [r for r in DATA.get("travel_reservations", []) if r.get("order_id") == order_id]
    order_docs = [d for d in DATA.get("documents", []) if d.get("order_id") == order_id]
    order_endpoints = [e for e in DATA.get("order_endpoint_details", []) if e.get("order_id") == order_id]
    order_asgs = [a for a in DATA.get("work_assignments", []) if a.get("order_id") == order_id and a.get("status") != "CANCELLED"]

    checks = []
    if order_asgs:
        checks.append("Driver assigned and dispatch confirmed")
    else:
        checks.append("Pending driver assignment / open marketplace")
        
    if order_tracks:
        checks.append(f"GPS telemetry verified active ({len(order_tracks)} observations recorded)")
    else:
        checks.append("GPS telemetry beacon standby")
        
    if order_res:
        checks.append(f"Maritime ferry booking confirmed ({order_res[0].get('provider', 'Carrier')})")
    else:
        checks.append("No maritime transit required on domestic route")
        
    if order_docs:
        checks.append(f"CMR Waybill: {order_docs[0].get('status', 'DRAFT')} ({order_docs[0].get('medium', 'DIGITAL')})")
    else:
        checks.append("Standard digital handover protocol enabled")
        
    if order_endpoints:
        checks.append("Pickup site contact and hours validated")
    else:
        checks.append("Site arrival inspection pending")

    return {
        "needs_human": needs_human,
        "category": category,
        "severity": severity,
        "headline": headline,
        "open_alerts": alerts,
        "active_incidents": incidents,
        "pending_proposals": proposals,
        "open_claims": claims,
        "open_work_items": open_work_items,
        "what_was_checked": checks
    }"""

new_attention = """    issue_info = get_clean_issue_info(incidents, alerts, proposals, claims, open_work_items) if needs_human else {
        "short_title": "On Track",
        "full_description": "On track - automated operations active"
    }
    short_title = issue_info["short_title"]
    full_description = issue_info["full_description"]

    # Pre-flight real checklist derived from actual data
    order_tracks = [t for t in DATA.get("tracking_observations", []) if t.get("order_id") == order_id]
    order_res = [r for r in DATA.get("travel_reservations", []) if r.get("order_id") == order_id]
    order_docs = [d for d in DATA.get("documents", []) if d.get("order_id") == order_id]
    order_endpoints = [e for e in DATA.get("order_endpoint_details", []) if e.get("order_id") == order_id]
    order_asgs = [a for a in DATA.get("work_assignments", []) if a.get("order_id") == order_id and a.get("status") != "CANCELLED"]

    checks = []
    if order_asgs:
        checks.append("Driver assigned and dispatch confirmed")
    else:
        checks.append("Pending driver assignment / open marketplace")
        
    if order_tracks:
        checks.append(f"GPS telemetry verified active ({len(order_tracks)} observations recorded)")
    else:
        checks.append("GPS telemetry beacon standby")
        
    if order_res:
        checks.append(f"Maritime ferry booking confirmed ({order_res[0].get('provider', 'Carrier')})")
    else:
        checks.append("No maritime transit required on domestic route")
        
    if order_docs:
        checks.append(f"CMR Waybill: {order_docs[0].get('status', 'DRAFT')} ({order_docs[0].get('medium', 'DIGITAL')})")
    else:
        checks.append("Standard digital handover protocol enabled")
        
    if order_endpoints:
        checks.append("Pickup site contact and hours validated")
    else:
        checks.append("Site arrival inspection pending")

    return {
        "needs_human": needs_human,
        "category": category,
        "severity": severity,
        "headline": short_title,
        "short_title": short_title,
        "full_description": full_description,
        "open_alerts": alerts,
        "active_incidents": incidents,
        "pending_proposals": proposals,
        "open_claims": claims,
        "open_work_items": open_work_items,
        "what_was_checked": checks
    }"""

assert "def get_order_attention" in content
content = content.replace(old_attention, new_attention)

with open(backend_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated backend issue info successfully.")
