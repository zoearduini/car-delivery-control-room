with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos1 = text.find('id="view-car-detail"')
pos2 = text.find('id="view-inbox"')
detail_html = text[pos1:pos2]
print("Car detail chunk length:", len(detail_html))
