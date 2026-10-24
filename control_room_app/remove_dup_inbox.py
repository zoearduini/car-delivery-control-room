with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """@app.get("/api/support-inbox")
def get_support_inbox():
    threads = DATA.get("support_inbox_threads", [])
    messages = DATA.get("support_inbox_messages", [])
    
    thread_map = []
    for t in threads:
        t_msgs = [m for m in messages if m.get("thread_id") == t.get("id")]
        t_msgs.sort(key=lambda m: m.get("authored_at", ""))
        
        t_copy = dict(t)
        t_copy["messages"] = t_msgs
        thread_map.append(t_copy)
        
    return {"threads": thread_map}"""

if target not in text:
    target = target.replace("\n", "\r\n")

assert target in text, "Duplicate get_support_inbox target not found"
text = text.replace(target, "", 1)

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Removed duplicate get_support_inbox successfully!")
