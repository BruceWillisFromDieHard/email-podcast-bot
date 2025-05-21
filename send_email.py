import os
import smtplib
from email.message import EmailMessage

def send_email_with_attachment():
    msg = EmailMessage()
    msg['Subject'] = "Your Daily Inbox Podcast 🎧"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECIPIENT")
    msg.set_content("Attached is your morning inbox podcast recap.")

    filepath = "daily_email_recap.mp3"
    with open(filepath, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='audio', subtype='mp3', filename=filepath)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)