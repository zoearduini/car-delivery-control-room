import urllib.request
import json

res = urllib.request.urlopen("http://127.0.0.1:8000/api/orders?filter=needs_attention")
data = json.loads(res.read())

print(f"Total needs_attention: {len(data)}")
for o in data:
    cat = o.get("attention", {}).get("category", "")
    print(f"{o['id']}: [{cat}] -> {o['headline']}")
