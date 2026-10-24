with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos1 = text.find('id="view-car-detail"')
pos2 = text.find('id="view-inbox"')
detail_html = text[pos1:pos2]

import re
comments = re.findall(r'<!--(.*?)-->', detail_html)
for c in comments:
    if any(k in c.lower() for k in ['tab', 'header', 'section', 'view', 'card']):
        print('Comment:', c.strip())
