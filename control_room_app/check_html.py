import re

index_path = "control_room_app/static/index.html"

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

print("HTML read successfully, length:", len(html))
