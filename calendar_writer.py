from ics import Calendar, Event as ICSEvent
from datetime import timedelta

def write_event_to_ics(event, filename="my_calendar.ics"):
    cal = Calendar()
    e = ICSEvent()

    e.name = event.title
    e.begin = event.start_time
    e.location = event.location or ""

    # 如果没有结束时间，默认 1 小时
    if event.end_time:
        e.end = event.end_time
    else:
        e.end = event.start_time + timedelta(hours=1)

    e.description = event.original_text

    cal.events.add(e)

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(cal)

    return filename