from datetime import datetime, timedelta, timezone

def get_time_window():
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=11, minutes=30)).replace(microsecond=0)
    return start.isoformat()

def fetch_emails():
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.body-content-type="text"',
    }

    since_time = get_time_window()
    url = f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/mailFolders/Inbox/messages?$top=200&$filter=receivedDateTime ge {since_time}"

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