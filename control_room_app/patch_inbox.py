with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "def get_support_inbox():"
func_start = text.find(target)
func_end = text.find("@app.post(\"/api/support-inbox/{thread_id}/link\")")

new_func = """def get_support_inbox():
    threads = DATA.get("support_inbox_threads", [])
    messages = DATA.get("support_inbox_messages", [])
    drivers_map = {d.get("id"): d for d in DATA.get("drivers", [])}
    customers_map = {c.get("id"): c for c in DATA.get("customers", [])}

    topic_names = {
        "travel_and_assignment": "Driver Duty & Schedule Inquiry",
        "document_request": "Handover Document Copy Request",
        "expense_payout": "Highway & Parking Expense Claim",
        "order_status": "External Dealership Status Inquiry",
        "general_policy": "Driver Expense Process Guidance"
    }

    formatted_threads = []
    for t in threads:
        t_msgs = [m for m in messages if m.get("thread_id") == t.get("id")]
        t_msgs.sort(key=lambda m: m.get("authored_at", ""))
        
        cp_id = t.get("counterparty_id")
        cp_type = t.get("counterparty_type", "driver")
        sender_name = cp_id or "Anonymous"
        sender_role = "Assigned Driver" if cp_type == "driver" else "Dealership Client"
        
        if cp_type == "driver" and cp_id in drivers_map:
            sender_name = drivers_map[cp_id].get("display_name", cp_id)
        elif cp_type == "customer" and cp_id in customers_map:
            sender_name = customers_map[cp_id].get("name", cp_id)

        # Candidate orders information
        cand_orders = []
        for cid in t.get("candidate_order_ids", []):
            o = next((ord for ord in DATA.get("orders", []) if ord["id"] == cid), None)
            if o:
                v = get_vehicle_for_order(cid)
                cand_orders.append({
                    "id": cid,
                    "reference": o.get("reference"),
                    "vehicle": f"{v.get('make')} {v.get('model')}" if v else "Vehicle",
                    "status": o.get("status")
                })

        formatted_threads.append({
            "id": t.get("id"),
            "status": t.get("status"),
            "link_state": t.get("link_state"),
            "category": t.get("category"),
            "topic_title": topic_names.get(t.get("category", ""), "Operations Support Message"),
            "sender_name": sender_name,
            "sender_role": sender_role,
            "sender_type": cp_type,
            "channel": t.get("channel", "app_chat"),
            "candidate_basis": t.get("candidate_basis"),
            "waiting_on": t.get("waiting_on"),
            "owner": t.get("owner"),
            "candidate_orders": cand_orders,
            "messages": t_msgs
        })

    return {
        "total_threads": len(formatted_threads),
        "open_threads": len([t for t in formatted_threads if t["status"] == "OPEN"]),
        "threads": formatted_threads
    }

"""

text = text[:func_start] + new_func + text[func_end:]

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated get_support_inbox successfully!")
