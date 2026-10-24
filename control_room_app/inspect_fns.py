with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_fn(name):
    print(f"\n==================== {name} ====================")
    found = False
    count = 0
    for i, line in enumerate(lines):
        if f"def {name}" in line or f"async def {name}" in line:
            found = True
            for j in range(max(0, i-2), min(len(lines), i+80)):
                print(lines[j], end="")
            break

print_fn("run_autonomous_agent")
print_fn("submit_decision")
