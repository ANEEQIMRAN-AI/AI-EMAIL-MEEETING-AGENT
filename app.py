# app.py
import streamlit as st
from email_reader import get_latest_emails
from summerizer import summarize_email
from meeting_extractor import extract_meeting_info
from calendar_writer import add_event_to_calendar

st.set_page_config(page_title="Email Insight Agent", layout="centered")
st.title("📩 Email Insight Agent")
st.markdown("Automatically read, summarize, and schedule meetings from your latest emails.")

if st.button("🔄 Fetch & Analyze Latest Emails"):
    with st.spinner("Connecting to Gmail and analyzing emails..."):
        emails = get_latest_emails(5)

        for i, email in enumerate(emails, 1):
            st.markdown(f"### ✉️ Email {i}: {email['subject']}")
            st.text(f"From: {email['from']} | Date: {email['date']}")

            summary = summarize_email(email['body'])
            st.markdown("**🧠 Summary:**")
            st.success(summary)

            meeting = extract_meeting_info(email['body'])
            if meeting:
                st.markdown("**📅 Meeting Detected:**")
                st.code(str(meeting))

                if st.button(f"🗓️ Add to Calendar (Email {i})"):
                    filepath = add_event_to_calendar(meeting)
                    st.success(f"Event saved: {filepath}")
            else:
                st.warning("No meeting detected in this email.")
