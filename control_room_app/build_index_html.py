import os

# We will read the existing index.html and update the components cleanly.
with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    orig_html = f.read()

print("Original length:", len(orig_html))
