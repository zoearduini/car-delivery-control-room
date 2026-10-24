with open("control_room_app/backend.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''    headline = get_clean_issue_description(incidents, alerts, proposals, claims, open_work_items) if needs_human else "On track  -  automated operations active"'''

replacement = '''    issue_info = get_clean_issue_info(incidents, alerts, proposals, claims, open_work_items) if needs_human else {
        "short_title": "On Track",
        "full_description": "On track - automated operations active"
    }
    short_title = issue_info["short_title"]
    full_description = issue_info["full_description"]'''

assert target in text, "Target headline line not found"
text = text.replace(target, replacement, 1)

target2 = '''    return {
        "needs_human": needs_human,
        "category": category,
        "severity": severity,
        "headline": headline,'''

replacement2 = '''    return {
        "needs_human": needs_human,
        "category": category,
        "severity": severity,
        "headline": short_title,
        "short_title": short_title,
        "full_description": full_description,'''

assert target2 in text, "Target return dict not found"
text = text.replace(target2, replacement2, 1)

with open("control_room_app/backend.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Replaced successfully!")
