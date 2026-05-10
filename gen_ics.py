import csv
from datetime import datetime

ics_template = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//OpenClaw//Yuihan Schedule//CN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:悦寒 IG课表
X-WR-TIMEZONE:Asia/Shanghai
{events}END:VCALENDAR"""

event_template = """BEGIN:VEVENT
UID:{uid}@4100751-yuihan-calendar
DTSTAMP:{dtstamp}Z
DTSTART;TZID=Asia/Shanghai:{start}
DTEND;TZID=Asia/Shanghai:{end}
SUMMARY:{summary}
DESCRIPTION:{desc}
LOCATION:{location}
CATEGORIES:{category}
STATUS:CONFIRMED
END:VEVENT"""

category_colors = {
    "数学": "🟠", "物理": "🟢", "化学": "🔵", "计算机": "🟣",
    "刷题研习": "🟪", "经济": "🟣", "EFL": "🟠",
    "IG考试": "🔴", "EOY模拟考": "🟠",
    "IG化学 42": "🔴", "IG数学 P1": "🔴", "IG化学 62": "🔴",
    "IG物理 42": "🔴", "IG数学 S1": "🔴", "IG计算机 12": "🔴",
    "IG物理 62": "🔴", "IG计算机 22": "🔴", "IG经济 22": "🔴",
    "IG物理 22": "🔴", "IG经济 12": "🔴", "IG化学 22": "🔴"
}

location_map = {"澳优": "澳优", "网课": "网课", "校内": "校内", "线上": "澳优"}

events = []
counter = 1

with open("yuihan_schedule_2026_v3.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        date, weekday, start_time, end_time, content, category, location = row
        date_str = date.replace("-", "")
        start_str = date_str + "T" + start_time.replace(":", "") + "00"
        end_str = date_str + "T" + end_time.replace(":", "") + "00"
        emoji = category_colors.get(content, "🟣")
        location_display = location_map.get(location, location)
        desc_map = {
            "数学": "IG数学常规课", "物理": "IG物理常规课",
            "化学": "IG化学常规课", "计算机": "IG计算机课",
            "刷题研习": "刷题研习课", "经济": "IG经济课"
        }
        desc = desc_map.get(content, content)
        uid = f"ev{counter:03d}-{date_str}@{4100751}-yuihan-calendar"
        counter += 1
        events.append(event_template.format(
            uid=uid,
            dtstamp=datetime.now().strftime("%Y%m%dT%H%M%S"),
            start=start_str,
            end=end_str,
            summary=f"{emoji} {content}" if not content.startswith("IG") else content,
            desc=desc,
            location=location_display,
            category=category
        ))

with open("yuihan_schedule.ics", "w", encoding="utf-8") as f:
    f.write(ics_template.format(events="\n".join(events)))

print(f"Generated {len(events)} events")
