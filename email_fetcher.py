import os
from dotenv import load_dotenv
from msal import PublicClientApplication
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import email.utils

load_dotenv()

# === Custom rules ===
CLIENT_DOMAINS = ["@skmediagroup.com.au", "@aria.com.au"]
INTERNAL_SENDERS = ["andrew@skmediagroup.com.au"]
NEWS_SOURCES = ["@newyorker.com", "@nytimes.com", "@monocle.com", "@puck.news", "@substack.com"]
SHOPPING_DOMAINS = ["@farfetch.com", "@ssense.com", "@theiconic.com.au", "@shop.", "@norse", "@matchesfashion"]
STREAM_KEYWORDS = ["7West Media", "ARIA"]

now = datetime.now()
eight_pm_yesterday = (now - timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0)

def classify_email(sender, subject, body):
    sender_lower = sender.lower()

    if any(domain in sender_lower for domain in SHOPPING_DOMAINS):
        return "shopping"
    if any(domain in sender_lower for domain in NEWS_SOURCES):
        return "news"
    if "stream" in sender_lower:
        if any(keyword.lower() in body.lower() for keyword in STREAM_KEYWORDS):
            return "stream_corp"
        else:
            return "stream_other"
    if any(domain in sender_lower for domain in CLIENT_DOMAINS):
        return "client"
    if sender_lower in INTERNAL_SENDERS:
        return "internal"
    if any(word in subject.lower() for word in ["urgent", "action required", "asap", "important"]):
        return "urgent"
    return "general"

def extract_sender_name(sender_str):
    if "<" in sender_str and ">" in sender_str:
        return sender_str.split("<")[0].strip()
    if "@" in sender_str:
        return sender_str.split("@")[0].split(".")[0].capitalize()
    return sender_str.strip()

def fetch_emails():
    client_id = os.getenv("MS_CLIENT_ID")
    tenant_id = os.getenv("MS_TENANT_ID")
    user_email = os.getenv("MS_EMAIL")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["Mail.Read"]

    app = PublicClientApplication(client_id=client_id, authority=authority)

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scope, account=accounts[0])
    else:
        flow = app.initiate_device_flow(scopes=scope)
        if "user_code" not in flow:
            raise Exception("❌ Failed to initiate device flow")
        print(f"🔐 Go to {flow['verification_uri']} and enter code: {flow['user_code']}")
        print("⏳ Waiting for authentication...")
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        print(f"🛑 Token response from Microsoft:\n{result}")
        raise Exception("❌ Failed to authenticate with Microsoft Graph")

    headers = {
        'Authorization': f"Bearer {result['access_token']}",
        'Content-Type': 'application/json'
    }

    start_time = eight_pm_yesterday.isoformat()
    print(f"📡 Fetching last 100 messages from inbox, filtering in Python since {start_time}")

    inbox_url = f'https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/inbox/messages?$orderby=receivedDateTime desc&$top=100'
    try:
        inbox_resp = requests.get(inbox_url, headers=headers)
        inbox_resp.raise_for_status()
    except Exception as e:
        print(f"⚠️ Failed to fetch or parse inbox response: {e}")
        return []

    data = inbox_resp.json()
    emails = []

    for msg in data.get('value', []):
        subject = msg.get('subject') or "(No Subject)"
        sender_full = msg.get('from', {}).get('emailAddress', {}).get('name') or msg.get('from', {}).get('emailAddress', {}).get('address') or "(Unknown Sender)"
        sender = extract_sender_name(sender_full)
        body = msg.get('body', {}).get('content') or ""
        date_str = msg.get('receivedDateTime')

        try:
            received_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        except:
            try:
                received_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                received_dt = now

        if received_dt < eight_pm_yesterday:
            continue

        try:
            body = BeautifulSoup(body, "html.parser").get_text()
        except Exception:
            pass

        tag = classify_email(sender_full, subject, body)

        emails.append({
            'subject': subject.strip(),
            'sender': sender.strip(),
            'body': body.strip(),
            'received': received_dt.isoformat(),
            'tag': tag
        })

    print(f"📨 Total emails after filtering: {len(emails)}")
    return emails
