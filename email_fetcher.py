import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
TENANT_ID = os.getenv("MS_TENANT_ID")
USER_EMAIL = os.getenv("MS_USER_EMAIL")

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
    else:
        raise Exception(f"❌ Token fetch failed: {result.get('error_description')}")

def fetch_emails():
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.body-content-type="text"',
    }

    now = datetime.now()
    start_time = (now - timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0)
    end_time = now.replace(microsecond=0)

    filter_query = f"receivedDateTime ge {start_time.isoformat()} and receivedDateTime le {end_time.isoformat()}"
    url = f"{GRAPH_API_ENDPOINT}/users/{USER_EMAIL}/mailFolders/inbox/messages?$top=200&$orderby=receivedDateTime desc&$filter={filter_query}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"❌ Graph API error: {response.status_code} - {response.text}")

    messages = response.json().get("value", [])
    emails = [
        {
            "subject": msg.get("subject", ""),
            "from": msg.get("from", {}).get("emailAddress", {}).get("address", "Unknown"),
            "body": msg.get("body", {}).get("content", ""),
            "received": msg.get("receivedDateTime", ""),
        }
        for msg in messages
    ]
    return emails