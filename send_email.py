import os
import smtplib
from email.message import EmailMessage

def send_email_with_attachment(filepath):
    msg = EmailMessage()
    msg["Subject"] = "Your Daily Email Podcast"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")
    msg.set_content("Attached is your morning email podcast.")

    with open(filepath, "rb") as f:
        data = f.read()
        msg.add_attachment(data, maintype="audio", subtype="mpeg", filename=filepath)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)