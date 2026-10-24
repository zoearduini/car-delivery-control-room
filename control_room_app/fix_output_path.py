with open("control_room_app/build_clean_frontend.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("with open(output_path", "output_path = 'control_room_app/static/index.html'\nwith open(output_path")

with open("control_room_app/build_clean_frontend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated build_clean_frontend.py")
