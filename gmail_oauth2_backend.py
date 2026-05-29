import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class GmailOAuth2Backend(BaseEmailBackend):

    def send_messages(self, email_messages):
        creds = Credentials(
            token=None,
            refresh_token=settings.GMAIL_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GMAIL_CLIENT_ID,
            client_secret=settings.GMAIL_CLIENT_SECRET,
        )
        creds.refresh(Request())
        service = build("gmail", "v1", credentials=creds)

        sent_count = 0
        for message in email_messages:
            try:
                mime_message = MIMEMultipart("alternative")
                mime_message["Subject"] = message.subject
                mime_message["From"] = settings.DEFAULT_FROM_EMAIL
                mime_message["To"] = ", ".join(message.to)

                mime_message.attach(MIMEText(message.body, "plain"))

                raw = base64.urlsafe_b64encode(
                    mime_message.as_bytes()
                ).decode()

                service.users().messages().send(
                    userId="me", body={"raw": raw}
                ).execute()

                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e

        return sent_count
