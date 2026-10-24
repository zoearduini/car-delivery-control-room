with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', text))

pos = text.find("<script>")
js_code = text[pos:]

get_ids = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_code)

print("Total getElementById calls:", len(get_ids))
missing = [gid for gid in get_ids if gid not in all_ids]
print("Missing IDs called by getElementById:", set(missing))
