from datetime import datetime
from collections import defaultdict

def summarize_emails(emails):
    summaries = []

    # === Group emails by type ===
    buckets = defaultdict(list)
    for email in emails:
        buckets[email['tag']].append(email)

    # === Start with urgent emails ===
    if buckets['urgent']:
        summaries.append("🚨 Urgent Updates:")
        for e in buckets['urgent']:
            summaries.append(f"From {e['sender']}: {e['subject']}")

    # === Internal and Client Emails ===
    important_internal = buckets['internal']
    important_clients = buckets['client']
    if important_internal or important_clients:
        summaries.append("📂 Work Highlights:")
        if important_internal:
            summaries.append("🔧 Internal SKMG team activity:")
            topics = set()
            for e in important_internal:
                topics.add(e['subject'])
            summaries.extend([f"- {t}" for t in list(topics)[:3]])
        if important_clients:
            summaries.append("🤝 Client discussions:")
            topics = set()
            for e in important_clients:
                topics.add(e['subject'])
            summaries.extend([f"- {t}" for t in list(topics)[:3]])

    # === Newsletter coverage ===
    priority_news = []
    general_news = []
    substacks = []

    for e in buckets['news']:
        sender = e['sender'].lower()
        if any(x in sender for x in ["newyorker", "nytimes", "monocle", "puck"]):
            priority_news.append(e)
        elif "substack" in sender:
            substacks.append(e)
        else:
            general_news.append(e)

    if priority_news:
        summaries.append("📰 Top Reads:")
        for e in priority_news[:3]:
            summaries.append(f"From {e['sender']}: {e['subject']}")

    if any(s['subject'].lower().startswith("re:") for s in substacks):
        summaries.append("✉️ Substack threads:")
        for e in substacks[:2]:
            summaries.append(f"{e['sender']}: {e['subject']}")

    if general_news:
        summaries.append("📢 Other updates:")
        for e in general_news[:2]:
            summaries.append(f"{e['sender']}: {e['subject']}")

    # === Misc ===
    general = buckets['general']
    if general:
        summaries.append("📌 Miscellaneous mentions:")
        for e in general[:2]:
            summaries.append(f"{e['sender']}: {e['subject']}")

    return summaries
