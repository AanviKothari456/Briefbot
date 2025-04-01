from calendar_service import get_latest_past_meeting
from docs_service import get_doc_id_by_title, get_doc_content
from summarizer import summarize_text
from email_service import send_email
import time


def run_summary_and_send():
    print("🔍 Fetching latest meeting...")
    event = get_latest_past_meeting()
    if not event:
        print("❌ No recent meetings found.")
        return

    title = event['summary']
    attendees = [a['email'] for a in event.get('attendees', []) if 'email' in a]
    start_time = event['start']['dateTime']

    print(f"📄 Finding doc for meeting: {title}")
    doc_id = get_doc_id_by_title(title)
    if not doc_id:
        print("❌ No matching Google Doc found.")
        return

    print("📥 Reading document content...")
    doc_text = get_doc_content(doc_id)

    print("🤖 Summarizing with Claude...")
    summary = summarize_text(doc_text)

    print("✉️ Sending summary to attendees...")
    send_email(
        recipients=attendees,
        subject=f"Meeting Summary: {title} ({start_time})",
        body=summary,
        attachment_url=f"https://docs.google.com/document/d/{doc_id}"
    )


if __name__ == "__main__":
    # Simulate scheduled call (can be triggered via cron or APScheduler)
    run_summary_and_send()