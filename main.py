from dotenv import load_dotenv
load_dotenv()

from email_fetcher import fetch_emails
from summarizer import summarize_emails
from narrator import create_audio
from send_email import send_email_with_attachment
import traceback
import subprocess

def main():
    print("✅ Script started!")
    print("📥 Step 1: Fetching emails...")

    try:
        emails = fetch_emails()
        print(f"📨 Fetched {len(emails)} emails.")

        summaries = summarize_emails(emails)

        if summaries:
            print("🎧 Step 3: Creating audio...")
            filename = create_audio(summaries)

            print("📤 Step 4: Sending via email...")
            send_email_with_attachment(filename)
        else:
            print("📭 No podcast created — no relevant emails in time window.")

    except Exception as e:
        print("❌ An error occurred:")
        print(str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()