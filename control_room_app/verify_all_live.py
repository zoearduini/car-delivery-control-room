import urllib.request
import json
import time

time.sleep(2)
base = "http://127.0.0.1:8000"

print("1. Testing /api/stats...")
with urllib.request.urlopen(f"{base}/api/stats") as r:
    stats = json.loads(r.read())
    print("   Total orders:", stats["total_orders"], "Needs attention:", stats["needs_human_count"], "On track:", stats["on_track_count"])
    assert stats["total_orders"] == 100
    assert stats["needs_human_count"] == 22

print("2. Testing /api/orders...")
with urllib.request.urlopen(f"{base}/api/orders?status_filter=all") as r:
    orders = json.loads(r.read())
    print("   Total orders returned:", len(orders))
    assert len(orders) == 100
    sample_issue = next(o for o in orders if o["attention"]["needs_human"])
    print("   Sample short_title:", sample_issue["attention"]["short_title"])
    assert len(sample_issue["attention"]["short_title"].split()) <= 6

print("3. Testing ord-00322 details...")
with urllib.request.urlopen(f"{base}/api/orders/ord-00322") as r:
    det_322 = json.loads(r.read())
    coords = det_322["addresses"]["coordinates"]
    print("   Driven geom waypoints:", len(coords["driven_geometry"]))
    print("   Remaining geom waypoints:", len(coords["remaining_geometry"]))
    print("   Intermediate stops:", coords["intermediate_stops"])
    print("   Deal value:", det_322["deal"]["contract_value_eur"])
    assert len(coords["driven_geometry"]) > 0
    assert len(coords["remaining_geometry"]) > 0
    assert len(coords["intermediate_stops"]) > 0

print("4. Testing ord-00194 details & attachments...")
with urllib.request.urlopen(f"{base}/api/orders/ord-00194") as r:
    det_194 = json.loads(r.read())
    docs_with_file = [d for d in det_194["documents"] if d["has_file"]]
    exp_with_file = [e for e in det_194["expenses"] if e["has_file"]]
    print("   Docs with file:", len(docs_with_file), docs_with_file[0]["file_url"])
    print("   Expenses with receipt:", len(exp_with_file), exp_with_file[0]["receipt_url"])
    assert len(docs_with_file) > 0
    assert len(exp_with_file) > 0

    # Test PDF retrieval
    pdf_url = f"{base}{docs_with_file[0]['file_url']}"
    with urllib.request.urlopen(pdf_url) as pdf_r:
        print("   PDF fetch status:", pdf_r.status, "content-type:", pdf_r.headers.get("content-type"))
        assert pdf_r.status == 200

print("5. Testing /api/support-inbox...")
with urllib.request.urlopen(f"{base}/api/support-inbox") as r:
    inbox = json.loads(r.read())
    print("   Total inbox threads:", len(inbox["threads"]))
    print("   Thread 0 sender:", inbox["threads"][0]["sender_name"], "| topic:", inbox["threads"][0]["topic_title"])
    assert len(inbox["threads"]) > 0
    assert "topic_title" in inbox["threads"][0]

print("6. Testing frontend index.html...")
with urllib.request.urlopen(f"{base}/") as r:
    html = r.read().decode("utf-8")
    assert "car-section-deal" in html
    assert "car-section-route" in html
    assert "car-section-docs" in html
    assert "car-section-ferry" in html
    assert "car-section-chat" in html
    assert "car-section-actions" in html
    assert "universal-file-modal" in html
    assert "file-modal-iframe" in html
    assert "Credits" in html and "Available Credits:" in html
    print("   All frontend sections verified in index.html!")

print("\nALL 6 ENDPOINT AND UI VERIFICATIONS PASSED WITH 100% SUCCESS!")
