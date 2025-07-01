# 📬 AI Email-to-Calendar Assistant

This project is an **intelligent AI agent** that reads your latest Gmail emails using the **Gmail API**, extracts key points and meeting details with **Google Gemini LLM** via **LangChain**, and automatically schedules meetings with reminders on **Google Calendar**.

No manual copying. No missed meetings. Just smart, automated email-to-calendar scheduling. Built with LangChain, Gemini 1.5, and Google APIs.

---

## ✨ Features

- ✅ Reads your latest Gmail email (via Gmail API)
- 🧠 Summarizes email content using Gemini 1.5 LLM
- 📅 Extracts meeting subject, date, time, and location
- 🔔 Automatically schedules Google Calendar events with reminders
- 🔐 Uses secure OAuth2 authentication (no need for app passwords)
- 🧰 Built modularly using LangChain pipelines

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** – LLM orchestration
- **Google Gemini LLM** (via Makersuite API)
- **Gmail API** – to fetch latest emails
- **Google Calendar API** – to create calendar events
- **OAuth2 Authentication** – secure and modern auth
- **dotenv** – for API key and environment management

---

## 📂 Project Structure

ai-email-calendar-assistant/
├── main.py # Core orchestrator
├── gemini_parser.py # LLM pipeline logic (LangChain + Gemini)
├── credentials.json # Google OAuth client file (from Google Cloud)
├── token.json # Auto-generated after first login
├── .env # Gemini API key


---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-email-calendar-assistant.git
cd ai-email-calendar-assistant

Install Required Python Libraries
pip install langchain langchain-google-genai google-generativeai
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install python-dotenv


Add Your Gemini API Key
Visit 👉 https://makersuite.google.com/app/apikey

Copy your API key

Create a .env file in your root folder and add:

env
Copy
Edit
GOOGLE_API_KEY=your_gemini_api_key_here


Set Up Google Cloud Credentials
Go to 👉 https://console.cloud.google.com

Create a new project (e.g., AI Meeting Agent)

Enable these APIs:

Gmail API

Google Calendar API

Go to APIs & Services > Credentials

Click Create Credentials > OAuth Client ID

Application type: Desktop

Download the JSON file and rename it as:

pgsql
Copy
Edit
credentials.json

Place it in the project root folder


✅ How to Run the Agent
bash
Copy
Edit
python main.py
On first run, a browser will open to authenticate your Google account.

A file token.json will be saved to reuse the session.

The script will:

🔍 Read your latest email

🧠 Analyze it with Gemini

📅 Add meeting to Google Calendar (if found)


🧠 How It Works
Gmail API fetches the latest unread email.

The content is passed to Gemini 1.5 LLM through a LangChain prompt.

Gemini returns structured data:

json
Copy
Edit
{
  "summary": "Discussion on the new app launch.",
  "meeting_subject": "App Launch Meeting",
  "meeting_datetime": "2025-07-05 15:00",
  "location": "Zoom"
}
If a valid date and time are detected, it creates a Google Calendar event and sets a reminder 10 minutes before the meeting.

📩 Sample Email It Understands
Subject: App Launch

Hey Aneeq, just a reminder that we’ll meet on July 5 at 3:00 PM on Zoom to finalize the launch. See you there!

✔️ The system will:

Detect the date, time, and location

Add a calendar event titled App Launch Meeting

Set a 10-minute reminder

📌 Future Improvements
⏱️ Automatically run every 15–30 mins via scheduler

📨 Process multiple unread emails (batch mode)

📊 Add web dashboard for tracking meetings

💬 Integrate with voice assistants or chatbots

📄 License
MIT License © 2025 Aneeq Imran
