import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # typically same as SMTP_USERNAME


def send_email(recipients, subject, body, attachment_url=None):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body + (f"\n\nMeeting Notes: {attachment_url}" if attachment_url else ""))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", str(e))


if __name__ == "__main__":
    send_email(
        recipients=["alice@example.com", "bob@example.com"],
        subject="Meeting Summary: Project Sync",
        body="Here’s a summary of today’s meeting:",
        attachment_url="https://docs.google.com/document/d/your-doc-id"
    )
