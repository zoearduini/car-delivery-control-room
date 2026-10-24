import re

with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    code = f.read()

print("--- API ROUTES ---")
routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"\)', code)
for method, r in routes:
    print(f"{method.upper():6} {r}")

print("\n--- AGENT / TOOL FUNCTIONS ---")
funcs = re.findall(r'def\s+([a-zA-Z0-9_]*(?:agent|tool|action|approve|proposal|decision)[a-zA-Z0-9_]*)\s*\(', code)
for fn in set(funcs):
    print(f"Function: {fn}")
