with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos1 = text.find('id="view-inbox"')
pos2 = text.find('id="view-history"')
print("Inbox chunk length:", pos2 - pos1)
print(text[pos1:pos1+1200].replace('\u2192', '->').replace('\u2014', '-').replace('\u2022', '*'))
