from datetime import datetime, timedelta, timezone
import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
TENANT_ID = os.getenv("MS_TENANT_ID")
TARGET_USER = os.getenv("MS_USER_EMAIL")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

def get_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    raise Exception(f"❌ Token fetch failed: {result.get('error_description')}")

def get_time_window():
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=11, minutes=30)).replace(microsecond=0)
    return start.isoformat().replace("+00:00", "Z")

def fetch_emails():
    access_token = get_token()
    since_time = get_time_window()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.body-content-type="text"',
    }

    url = (
        f"{GRAPH_API_ENDPOINT}/users/{TARGET_USER}/mailFolders/inbox/messages"
        f"?$filter=receivedDateTime ge {since_time}"
        f"&$orderby=receivedDateTime desc&$top=200"
    )

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"❌ Graph API error: {response.status_code} – {response.text}")

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