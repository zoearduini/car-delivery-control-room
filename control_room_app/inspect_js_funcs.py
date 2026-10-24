with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("<script>")
js_text = text[pos:]

import re
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', js_text)
async_funcs = re.findall(r'async\s+function\s+([a-zA-Z0-9_]+)\s*\(', js_text)

print("Synchronous functions:", funcs)
print("Async functions:", async_funcs)
