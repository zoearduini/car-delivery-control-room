import urllib.request
import json

base = "http://127.0.0.1:8000"

# Note: server is currently running previous version until restarted,
# let's import directly from control_room_app.backend to test function outputs directly!
from control_room_app.backend import get_stats, list_orders, get_order_detail, get_support_inbox

stats = get_stats()
print("Stats needs_human:", stats["needs_human_count"], "total:", stats["total_orders"])

orders = list_orders("all", "all", "newest", "")
print("Total orders:", len(orders))
sample_issue = next(o for o in orders if o["attention"]["needs_human"])
print("Sample issue short title:", sample_issue["attention"]["short_title"])
print("Sample issue full desc:", sample_issue["attention"]["full_description"][:80])

det_322 = get_order_detail("ord-00322")
print("ord-00322 deal:", det_322.get("deal"))
print("ord-00322 intermediate_stops:", det_322["addresses"]["coordinates"]["intermediate_stops"])
print("ord-00322 driven geom count:", len(det_322["addresses"]["coordinates"]["driven_geometry"]))
print("ord-00322 remaining geom count:", len(det_322["addresses"]["coordinates"]["remaining_geometry"]))
print("ord-00322 docs count:", len(det_322["documents"]), "sample doc:", det_322["documents"][0] if det_322["documents"] else "none")
print("ord-00322 expenses count:", len(det_322["expenses"]), "sample expense:", det_322["expenses"][0] if det_322["expenses"] else "none")

det_194 = get_order_detail("ord-00194")
print("ord-00194 docs with file:", [d["file_name"] for d in det_194["documents"] if d["has_file"]])
print("ord-00194 expenses with receipt:", [e["file_name"] for e in det_194["expenses"] if e["has_file"]])

inbox = get_support_inbox()
print("Inbox threads count:", len(inbox["threads"]))
print("Sample thread sender:", inbox["threads"][0]["sender_name"], "topic:", inbox["threads"][0]["topic_title"])
