# calendar_writer.py
from datetime import datetime
from ics import Calendar, Event
import os

def add_event_to_calendar(meeting: dict, filename: str = "meeting_event.ics") -> str:
    cal = Calendar()
    event = Event()

    event.name = meeting.get("title", "Meeting")
    event.begin = meeting.get("datetime")
    event.location = meeting.get("location", "")
    event.duration = {"hours": 1}  # Default to 1-hour meeting

    cal.events.add(event)
    with open(filename, "w") as f:
        f.writelines(cal)

    # Return full path to file
    return os.path.abspath(filename)


if __name__ == "__main__":
    sample_meeting = {
        "title": "Team Strategy Session",
        "datetime": datetime.now().isoformat(),
        "location": "Zoom Link: https://zoom.us/xyz"
    }
    print("ICS file saved at:", add_event_to_calendar(sample_meeting))
