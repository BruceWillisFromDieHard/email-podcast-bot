from collections import defaultdict

def categorize_email(email):
    sender = email['from'].lower()
    subject = email['subject'].lower()

    if "skmediagroup.com.au" in sender or "client" in subject or "urgent" in subject:
        return "urgent"
    elif any(x in sender for x in ["@skmediagroup.com.au", "andrew@skmediagroup.com.au"]):
        return "internal"
    elif any(x in sender for x in ["@puck.news", "nytimes.com", "monocle.com"]):
        return "news"
    elif any(x in sender for x in ["@substack.com", "newsletter"]):
        return "newsletters"
    elif any(x in sender for x in ["farfetch", "ssense", "matchesfashion", "mrporter"]):
        return "marketing"
    else:
        return "default"

def summarize_emails(emails):
    print("🔍 Step 2: Summarizing emails...")

    buckets = defaultdict(list)

    for email in emails:
        tag = categorize_email(email)
        buckets[tag].append(email)

    summaries = []
    for tag, grouped_emails in buckets.items():
        summary = f"Summary for {len(grouped_emails)} emails in group '{tag}':\n"
        for email in grouped_emails:
            summary += f"• {email['subject']} (from {email['from']})\n"
        summaries.append(summary)

    return summaries