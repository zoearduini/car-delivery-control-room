import os, re

# Read current file
with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Let's inspect the global header bar in index.html
pos_header_start = orig.find('<!-- TOP GLOBAL HEADER BAR -->')
pos_header_end = orig.find('<!-- ================= VIEW 1: HOME (FLEET TABLE) ================= -->')
header_chunk = orig[pos_header_start:pos_header_end]
print("Header length:", len(header_chunk))
