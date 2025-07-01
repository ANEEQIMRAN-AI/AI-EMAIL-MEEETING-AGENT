# summarizer.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

summary_prompt = PromptTemplate.from_template("""
You are an intelligent assistant.
Summarize the following email in a concise and clear paragraph.
Only include the key points, important dates, or actions requested.

Email:

{email_body}


Summary:
""")

def summarize_email(email_body: str) -> str:
    response = gemini.invoke(summary_prompt.format(email_body=email_body))
    return response.content.strip()


if __name__ == "__main__":
    sample = """
    Hello team,
    Just a reminder that we have our Q2 strategy meeting next Wednesday at 3:00 PM in Conference Room A.
    Please review the attached documents beforehand.
    Best,
    Alex
    """
    print(summarize_email(sample))
