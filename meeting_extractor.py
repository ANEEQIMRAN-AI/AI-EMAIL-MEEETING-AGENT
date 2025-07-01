# meeting_extractor.py
import dateparser
import re
from typing import Optional, Dict


def extract_meeting_info(email_text: str) -> Optional[Dict[str, str]]:
    lines = email_text.splitlines()
    meeting_info = {
        "title": "Meeting",
        "datetime": None,
        "location": None
    }

    for line in lines:
        # Try to parse date/time from the line
        dt = dateparser.parse(line, settings={"PREFER_DATES_FROM": "future"})
        if dt and not meeting_info["datetime"]:
            meeting_info["datetime"] = dt.isoformat()

        # Try to find a location
        if ("room" in line.lower() or "zoom" in line.lower() or "meet" in line.lower()) and not meeting_info["location"]:
            meeting_info["location"] = line.strip()

        # Update title based on subject-like lines
        if any(keyword in line.lower() for keyword in ["meeting", "call", "sync", "discussion"]):
            meeting_info["title"] = line.strip()

    if meeting_info["datetime"]:
        return meeting_info
    else:
        return None


if __name__ == "__main__":
    test_email = """
    Subject: Weekly Sync
    Let's meet this Friday at 2:00 PM in Room 301 to discuss updates.
    """
    print(extract_meeting_info(test_email))
