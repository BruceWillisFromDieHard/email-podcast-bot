import os
import requests
from datetime import datetime, timedelta, timezone
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

TARGET_USER = os.getenv("MS_USER_EMAIL")

def get_token():
    app = ConfidentialClientApplication(
        client_id=os.getenv("MS_CLIENT_ID"),
        client_credential=os.getenv("MS_CLIENT_SECRET"),
        authority=f"https://login.microsoftonline.com/{os.getenv('MS_TENANT_ID')}",
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"❌ Token fetch failed: {result.get('error_description')}")

def get_time_window():
    now = datetime.now(timezone.utc)
    yesterday_8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    if now.hour < 7 or (now.hour == 7 and now.minute < 30):
        yesterday_8pm -= timedelta(days=1)
    return yesterday_8pm.isoformat()

def fetch_emails():
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.body-content-type="text"',
    }

    since_time = get_time_window()
    url = (
        f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/mailFolders/inbox/messages"
        f"?$filter=receivedDateTime ge {since_time}"
        f"&$orderby=receivedDateTime desc"
        f"&$top=200"
    )

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"❌ Graph API error: {response.status_code} - {response.text}")

    messages = response.json().get("value", [])
    return [
        {
            "subject": msg["subject"],
            "from": msg["from"]["emailAddress"]["name"],
            "body": msg["body"]["content"],
            "received": msg["receivedDateTime"],
        }
        for msg in messages
    ]