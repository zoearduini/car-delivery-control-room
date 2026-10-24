with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "def get_clean_issue_description(incidents, alerts, proposals, claims, work_items) -> str:"

func_def = """def get_clean_issue_info(incidents, alerts, proposals, claims, work_items) -> Dict[str, str]:
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
    return info["short_title"]
"""

# Let's replace the whole old get_clean_issue_description function
old_func_end = text.find("def get_order_attention")
old_func_start = text.find(target)
text = text[:old_func_start] + func_def + "\n\n" + text[old_func_end:]

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Inserted get_clean_issue_info successfully!")
