with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "    # Commercial Deal details\n    tw_pickup ="
replacement = "    # Commercial Deal details\n    order_tracks = [t for t in DATA.get('tracking_observations', []) if t.get('order_id') == order_id]\n    tw_pickup ="

if target not in text:
    target = target.replace("\n", "\r\n")
    replacement = replacement.replace("\n", "\r\n")

assert target in text, "Target not found"
text = text.replace(target, replacement, 1)

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Inserted order_tracks successfully!")
