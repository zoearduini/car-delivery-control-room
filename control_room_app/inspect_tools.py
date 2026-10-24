with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "class AgentToolExecutor" in line:
        for j in range(i, min(len(lines), i+120)):
            print(lines[j], end="")
        break
