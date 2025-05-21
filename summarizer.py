from collections import defaultdict
import re


def categorize_email(email):
    sender_email = email['from'].lower()
    sender_name = email.get('sender_name', '').lower()
    subject = email['subject'].lower()
    body = email['body'].lower()

    # Expanded and intelligent keyword sets
    urgent_keywords = [
        "urgent", "asap", "immediate", "important", "action required", "deadline",
        "critical", "issue", "problem", "resolve", "respond now", "attention needed",
        "must respond", "last chance", "payment due"
    ]

    internal_names = [
        "andrew", "gereurd", "skmg", "team", "internal", "monday note", "staff update",
        "check-in", "sync", "review", "note to team", "re: internal"
    ]

    news_sources = [
        "new yorker", "nytimes", "new york times", "monocle", "puck", "axios", "politico",
        "bloomberg", "reuters", "financial times", "ft.com", "techcrunch"
    ]

    newsletter_keywords = [
        "substack", "digest", "newsletter", "roundup", "dispatch", "briefing",
        "summary", "insights", "thoughts", "recap", "analysis", "reads"
    ]

    marketing_keywords = [
        "sale", "shop", "deal", "ssense", "farfetch", "exclusive", "offer", "discount",
        "limited time", "buy now", "save", "flash sale", "promotion", "special"
    ]

    if any(kw in subject or kw in body for kw in urgent_keywords):
        return "urgent"
    if any(name in sender_name or name in subject for name in internal_names):
        return "internal"
    if any(source in sender_email or source in sender_name for source in news_sources):
        return "news"
    if any(kw in subject or kw in body for kw in newsletter_keywords):
        return "newsletters"
    if any(kw in subject or sender_email for kw in marketing_keywords):
        return "marketing"

    return "default"


def summarize_emails(emails):
    print("🔍 Step 2: Summarizing emails...")

    buckets = defaultdict(list)
    for email in emails:
        tag = categorize_email(email)
        buckets[tag].append(email)

    summaries = []
    for tag, grouped_emails in buckets.items():
        summary_lines = []

        for email in grouped_emails:
            sender = re.sub(r'\s*<.*?>', '', email.get('from', ''))
            headline = email['subject'].strip().capitalize()
            snippet = email['body'].strip().split("\n")[0][:240].strip()

            line = f"• From {sender}: {headline}. {snippet}"
            summary_lines.append(line)

        summary_text = f"\n".join(summary_lines)
        summaries.append({
            "category": tag,
            "summary": summary_text
        })

    return summaries
