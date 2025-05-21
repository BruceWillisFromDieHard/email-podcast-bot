import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
TENANT_ID = os.getenv("MS_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Replace with the actual mailbox you'd like to read from
TARGET_USER = os.getenv("MS_USER_EMAIL")  # optional: create a new secret for this

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

    # Example: Get messages from a specific user’s inbox
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.body-content-type="text"',
    }

    # You can set a static user here or pass dynamically
    user_email = TARGET_USER or "your-user@domain.com"
    url = f"{GRAPH_API_ENDPOINT}/users/{user_email}/mailFolders/Inbox/messages?$top=10"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"❌ Graph API error: {response.status_code} - {response.text}")

    messages = response.json().get("value", [])
    emails = [
        {
            "subject": msg["subject"],
            "from": msg["from"]["emailAddress"]["name"],
            "body": msg["body"]["content"],
            "received": msg["receivedDateTime"],
        }
        for msg in messages
    ]

    return emails