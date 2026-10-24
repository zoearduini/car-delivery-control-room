with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def get_order_attention" in line:
        for j in range(i, min(len(lines), i+60)):
            print(lines[j], end="")
        break
