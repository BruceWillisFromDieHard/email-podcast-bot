from collections import defaultdict

def categorize_email(email):
    sender = email["from"].lower()
    subject = email["subject"].lower()

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

    # Sort emails into buckets
    buckets = defaultdict(list)
    for email in emails:
        tag = categorize_email(email)
        buckets[tag].append(email)

    # Order of importance
    priority_order = ["urgent", "internal", "news", "newsletters", "default", "marketing"]

    summaries = []

    for tag in priority_order:
        if tag not in buckets:
            continue

        grouped_emails = buckets[tag]

        # Custom intro per category
        if tag == "urgent":
            intro = "⚠️ Here's what you need to handle first:"
        elif tag == "internal":
            intro = "👥 Internal chatter and updates:"
        elif tag == "news":
            intro = "🗞️ Big stories from trusted outlets:"
        elif tag == "newsletters":
            intro = "📬 Newsletter nuggets worth noting:"
        elif tag == "marketing":
            intro = "🛍️ Brand fluff and shopping bait:"
        else:
            intro = "📩 Everything else hanging out in the inbox:"

        summary = f"{intro}\n"

        for email in grouped_emails:
            summary += f"• {email['subject']} (from {email['from']})\n"

        summaries.append({
            "category": tag,
            "summary": summary.strip()
        })

    return summaries