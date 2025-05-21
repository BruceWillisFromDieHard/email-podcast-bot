import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

msg = EmailMessage()
msg["Subject"] = "Test"
msg["From"] = os.getenv("EMAIL_FROM")
msg["To"] = os.getenv("EMAIL_TO")
msg.set_content("Test email")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
    smtp.send_message(msg)
    