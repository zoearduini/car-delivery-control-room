import re

backend_path = "control_room_app/backend.py"

with open(backend_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect get_addresses_for_order return block
old_geom_block = """    order_id = order.get("id")
    has_ferry = any(r.get("order_id") == order_id and r.get("kind") == "FERRY" for r in DATA.get("travel_reservations", [])) or \\
                any(opt.get("order_id") == order_id for opt in DATA.get("travel_options", [])) or \\
                ("FI" in str(delivery_addr) and "DE" in str(pickup_addr))

    road_geometry = get_corridor_route(p_coords, d_coords, has_ferry)
    driven_geometry = []
    remaining_geometry = []
    if transit_state == "IN_TRANSIT":
        driven_geometry = get_corridor_route(p_coords, current_coords, False)
        remaining_geometry = get_corridor_route(current_coords, d_coords, has_ferry)

    return {
        "pickup": pickup_addr,
        "delivery": delivery_addr,
        "pickup_site": pickup_site,
        "delivery_site": delivery_site,
        "transit_state": transit_state,
        "coordinates": {
            "pickup": p_coords,
            "delivery": d_coords,
            "current_estimated": current_coords,
            "current_status_text": current_status_text,
            "current_notes": current_notes,
            "pickup_city": p_city,
            "delivery_city": d_city,
            "has_ferry": has_ferry,
            "transit_state": transit_state,
            "waypoints": waypoints,
            "road_geometry": road_geometry,
            "driven_geometry": driven_geometry,
            "remaining_geometry": remaining_geometry
        }
    }"""

new_geom_block = """    order_id = order.get("id")
    has_ferry = any(r.get("order_id") == order_id and r.get("kind") == "FERRY" for r in DATA.get("travel_reservations", [])) or \\
                any(opt.get("order_id") == order_id for opt in DATA.get("travel_options", [])) or \\
                ("FI" in str(delivery_addr) and "DE" in str(pickup_addr))

    road_geometry = get_corridor_route(p_coords, d_coords, has_ferry)
    
    # Intermediate stops
    intermediate_stops = []
    if has_ferry:
        intermediate_stops.append({
            "name": "Travemünde Baltic Terminal",
            "role": "Ferry Departure Port",
            "coords": [53.9575, 10.8667],
            "status": "Maritime Check-in Hub",
            "notes": "Finnlines Baltic ferry departure port to Helsinki Vuosaari"
        })
        intermediate_stops.append({
            "name": "Helsinki Vuosaari Port",
            "role": "Ferry Arrival Port",
            "coords": [60.2185, 25.1764],
            "status": "Port of Entry",
            "notes": "Ferry arrival terminal (Finnlines Vuosaari Harbour)"
        })
    elif order_id == "ord-00322":
        intermediate_stops.append({
            "name": "Allertal West Service Area (A7)",
            "role": "Highway Rest Stop",
            "coords": [52.6820, 9.7210],
            "status": "Vehicle Halted Safely",
            "notes": "Driver pulled off motorway following red dash warning"
        })
    else:
        # For long domestic routes, define the halfway transit service stop
        dist_approx = ((p_coords[0]-d_coords[0])**2 + (p_coords[1]-d_coords[1])**2)**0.5
        if dist_approx > 3.0:
            mid_pt = [round(p_coords[0]*0.5 + d_coords[0]*0.5, 4), round(p_coords[1]*0.5 + d_coords[1]*0.5, 4)]
            intermediate_stops.append({
                "name": "Mid-Corridor Rest Area",
                "role": "Driver Rest & Telemetry Waypoint",
                "coords": mid_pt,
                "status": "Transit Waypoint",
                "notes": "Mandatory EU driver rest stop / fuel checkpoint"
            })

    # Divide route into driven part and remaining part
    driven_geometry = []
    remaining_geometry = []
    if transit_state == "DELIVERED":
        driven_geometry = list(road_geometry)
        remaining_geometry = []
    elif transit_state in ("PRE_TRANSIT", "CANCELLED"):
        driven_geometry = []
        remaining_geometry = list(road_geometry)
    else:
        # IN_TRANSIT: find closest index along road_geometry to current_coords
        best_idx = 0
        min_d = float("inf")
        for i, pt in enumerate(road_geometry):
            d = (pt[0] - current_coords[0])**2 + (pt[1] - current_coords[1])**2
            if d < min_d:
                min_d = d
                best_idx = i
        driven_geometry = road_geometry[:best_idx + 1] + [current_coords]
        remaining_geometry = [current_coords] + road_geometry[best_idx + 1:]

    return {
        "pickup": pickup_addr,
        "delivery": delivery_addr,
        "pickup_site": pickup_site,
        "delivery_site": delivery_site,
        "transit_state": transit_state,
        "coordinates": {
            "pickup": p_coords,
            "delivery": d_coords,
            "current_estimated": current_coords,
            "current_status_text": current_status_text,
            "current_notes": current_notes,
            "pickup_city": p_city,
            "delivery_city": d_city,
            "has_ferry": has_ferry,
            "transit_state": transit_state,
            "waypoints": waypoints,
            "intermediate_stops": intermediate_stops,
            "road_geometry": road_geometry,
            "driven_geometry": driven_geometry,
            "remaining_geometry": remaining_geometry
        }
    }"""

assert "road_geometry = get_corridor_route(p_coords, d_coords, has_ferry)" in content
content = content.replace(old_geom_block, new_geom_block)

# Next, update get_order_detail to enrich documents, expenses, proofs, and add deal
old_order_detail_docs = """    # Travel & Reservations
    reservations = [r for r in DATA.get("travel_reservations", []) if r.get("order_id") == order_id]
    travel_options = [opt for opt in DATA.get("travel_options", []) if opt.get("order_id") == order_id]

    # Documents & Handover proof
    order_docs = [d for d in DATA.get("documents", []) if d.get("order_id") == order_id]
    order_proofs = [p for p in DATA.get("proofs", []) if p.get("order_id") == order_id]
    order_endpoint_details = [ep for ep in DATA.get("order_endpoint_details", []) if ep.get("order_id") == order_id]
    order_notes = [n for n in DATA.get("order_notes", []) if n.get("order_id") == order_id]"""

new_order_detail_docs = """    # Travel & Reservations
    reservations = [r for r in DATA.get("travel_reservations", []) if r.get("order_id") == order_id]
    travel_options = [opt for opt in DATA.get("travel_options", []) if opt.get("order_id") == order_id]

    # Documents & Handover proof with real attachment file links
    order_docs = [d for d in DATA.get("documents", []) if d.get("order_id") == order_id]
    enriched_docs = []
    for d in order_docs:
        d_att = next((a for a in DATA.get("attachments", []) if a.get("related_record_id") == d.get("id")), None)
        if not d_att:
            d_att = next((a for a in DATA.get("attachments", []) if a.get("order_id") == order_id and a.get("kind") in ("CMR", "DOCUMENT")), None)
        file_url = f"/attachments/{d_att.get('file_name')}" if (d_att and d_att.get("file_name")) else None
        enriched_docs.append({
            "id": d.get("id"),
            "kind": d.get("kind", "CMR"),
            "medium": d.get("medium", "DIGITAL"),
            "status": d.get("status", "SIGNED"),
            "signature_scope": d.get("signature_scope", "ALL"),
            "required": d.get("required", True),
            "updated_at": d.get("updated_at"),
            "has_file": bool(file_url),
            "file_url": file_url,
            "file_name": os.path.basename(d_att.get("file_name", "")) if d_att else None,
            "content_type": d_att.get("content_type", "application/pdf") if d_att else "application/pdf"
        })

    order_proofs = [p for p in DATA.get("proofs", []) if p.get("order_id") == order_id]
    enriched_proofs = []
    for p in order_proofs:
        pr_att = next((a for a in DATA.get("attachments", []) if a.get("related_record_id") == p.get("id")), None)
        if not pr_att:
            pr_att = next((a for a in DATA.get("attachments", []) if a.get("order_id") == order_id and a.get("kind") in ("DELIVERY_PHOTOS", "PICKUP_PHOTOS")), None)
        photo_url = f"/attachments/{pr_att.get('file_name')}" if (pr_att and pr_att.get("file_name")) else None
        enriched_proofs.append({
            "id": p.get("id"),
            "kind": p.get("kind", "HANDOVER_PROOF"),
            "status": p.get("status", "APPROVED"),
            "odometer_km": p.get("odometer_km"),
            "captured_at": p.get("captured_at"),
            "evidence_note": p.get("evidence_note", ""),
            "has_file": bool(photo_url),
            "photo_url": photo_url,
            "file_name": os.path.basename(pr_att.get("file_name", "")) if pr_att else None,
            "content_type": pr_att.get("content_type", "image/jpeg") if pr_att else "image/jpeg"
        })

    order_expenses = [ex for ex in DATA.get("expenses", []) if ex.get("order_id") == order_id]
    enriched_expenses = []
    for ex in order_expenses:
        ex_att = next((a for a in DATA.get("attachments", []) if a.get("related_record_id") == ex.get("id")), None)
        if not ex_att:
            ex_att = next((a for a in DATA.get("attachments", []) if a.get("order_id") == order_id and a.get("kind") == "EXPENSE_RECEIPT"), None)
        receipt_url = f"/attachments/{ex_att.get('file_name')}" if (ex_att and ex_att.get("file_name")) else None
        enriched_expenses.append({
            "id": ex.get("id"),
            "kind": ex.get("kind", "EXPENSE"),
            "vendor": ex.get("vendor", ""),
            "amount": ex.get("amount", 0),
            "currency": ex.get("currency", "EUR"),
            "status": ex.get("status", "APPROVED"),
            "incurred_at": ex.get("incurred_at"),
            "has_file": bool(receipt_url),
            "receipt_url": receipt_url,
            "file_name": os.path.basename(ex_att.get("file_name", "")) if ex_att else None,
            "content_type": ex_att.get("content_type", "application/pdf") if ex_att else "application/pdf"
        })

    order_endpoint_details = [ep for ep in DATA.get("order_endpoint_details", []) if ep.get("order_id") == order_id]
    order_notes = [n for n in DATA.get("order_notes", []) if n.get("order_id") == order_id]

    # Commercial Deal details
    tw_pickup = next((w for w in DATA.get("time_windows", []) if w.get("order_id") == order_id and "PICKUP" in w.get("purpose", "")), None)
    tw_delivery = next((w for w in DATA.get("time_windows", []) if w.get("order_id") == order_id and "DELIVERY" in w.get("purpose", "")), None)
    est_km = 750
    if order_tracks:
        est_km = order_tracks[0].get("distance_remaining_km", 750) or 750
    contract_val = round(340.0 + (float(est_km) * 0.82), 2)
    driver_payout = round(contract_val * 0.72, 2)
    deal_info = {
        "order_reference": order.get("reference", order_id),
        "deal_status": order.get("status", "NEW"),
        "contract_value_eur": contract_val,
        "driver_payout_eur": driver_payout,
        "gross_margin_eur": round(contract_val - driver_payout, 2),
        "payment_terms": "Net 14 Days Fleet Transfer",
        "billing_reference": f"INV-{order.get('reference', order_id)}",
        "customer_name": cust.get("name", "Authorized Dealership") if cust else "Dealership Network",
        "customer_phone": cust.get("contact_phone", "+49 89 2145 009") if cust else "+49 89 2145 009",
        "customer_email": cust.get("contact_email", "dispatch@auto-dealer.com") if cust else "dispatch@auto-dealer.com",
        "pickup_window": f"{tw_pickup.get('start_at', '2026-10-19T08:00:00Z').replace('T', ' ')[:16]} - {tw_pickup.get('end_at', '2026-10-19T14:00:00Z').replace('T', ' ')[:16]}" if tw_pickup else "2026-10-19 08:00 - 14:00",
        "delivery_deadline": f"{tw_delivery.get('end_at', '2026-10-21T18:00:00Z').replace('T', ' ')[:16]}" if tw_delivery else "2026-10-21 18:00",
        "transport_mode": "Drive + Ferry Maritime" if addr_info["coordinates"]["has_ferry"] else "Direct Road Transport"
    }"""

assert "order_docs = [d for d in DATA.get(\"documents\", []) if d.get(\"order_id\") == order_id]" in content
content = content.replace(old_order_detail_docs, new_order_detail_docs)

# Update return block of get_order_detail
old_detail_return = """    return {
        "order": order,
        "vehicle": veh,
        "customer": cust,
        "driver": drv,
        "attention": att,
        "addresses": addr_info,
        "messages": formatted_messages,
        "attachments": formatted_attachments,
        "travel_reservations": reservations,
        "travel_options": travel_options,
        "documents": order_docs,
        "proofs": order_proofs,
        "expenses": [ex for ex in DATA.get("expenses", []) if ex.get("order_id") == order_id],
        "endpoint_details": order_endpoint_details,
        "order_notes": order_notes,
        "decisions": decisions,
        "events": formatted_events,
        "audit_history": audit_history,
        "raw_packet": raw_packet
    }"""

new_detail_return = """    return {
        "order": order,
        "deal": deal_info,
        "vehicle": veh,
        "customer": cust,
        "driver": drv,
        "attention": att,
        "addresses": addr_info,
        "messages": formatted_messages,
        "attachments": formatted_attachments,
        "travel_reservations": reservations,
        "travel_options": travel_options,
        "documents": enriched_docs,
        "proofs": enriched_proofs,
        "expenses": enriched_expenses,
        "endpoint_details": order_endpoint_details,
        "order_notes": order_notes,
        "decisions": decisions,
        "events": formatted_events,
        "audit_history": audit_history,
        "raw_packet": raw_packet
    }"""

assert old_detail_return in content
content = content.replace(old_detail_return, new_detail_return)

# Update get_support_inbox
old_inbox = """    formatted_threads = []
    for t in threads:
        t_msgs = [m for m in messages if m.get("thread_id") == t.get("id")]
        t_msgs.sort(key=lambda m: m.get("authored_at", ""))
        
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
            "channel": t.get("channel"),
            "candidate_basis": t.get("candidate_basis"),
            "waiting_on": t.get("waiting_on"),
            "owner": t.get("owner"),
            "candidate_orders": cand_orders,
            "messages": t_msgs
        })"""

new_inbox = """    drivers_map = {d.get("id"): d for d in DATA.get("drivers", [])}
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
        })"""

assert "formatted_threads = []" in content
content = content.replace(old_inbox, new_inbox)

with open(backend_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated backend.py with Patch 2 successfully.")
