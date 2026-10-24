with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos_start = text.find('id="view-car-detail"')
pos_end = text.find('id="view-inbox"')
car_detail_html = text[pos_start:pos_end]

import re
subsections = re.findall(r'id="([^"]+)"', car_detail_html)
print("IDs inside car-detail:", subsections)
