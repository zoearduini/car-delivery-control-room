with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''    # Documents & Handover proof
    order_docs = [d for d in DATA.get("documents", []) if d.get("order_id") == order_id]
    order_proofs = [p for p in DATA.get("proofs", []) if p.get("order_id") == order_id]
    order_endpoint_details = [ep for ep in DATA.get("order_endpoint_details", []) if ep.get("order_id") == order_id]
    order_notes = [n for n in DATA.get("order_notes", []) if n.get("order_id") == order_id]'''

replacement = '''    # Documents & Handover proof with real attachment file links
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
    }'''

assert target in text, "Target block not found"
text = text.replace(target, replacement, 1)

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated get_order_detail in backend.py successfully!")
