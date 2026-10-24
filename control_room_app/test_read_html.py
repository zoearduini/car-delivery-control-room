import os

with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    current_html = f.read()

print("Current index.html length:", len(current_html))
