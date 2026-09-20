import os
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def authenticate_gmail():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


gmail_service = authenticate_gmail()


from langchain.tools import tool


@tool
def send_email(
    recipients: list[str],
    subject: str,
    body: str
):
    """Send an email to multiple recipients."""

    message = MIMEText(body)

    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    gmail_service.users().messages().send(
        userId="me",
        body={
            "raw": encoded_message
        }
    ).execute()

    return f"Email sent successfully to {len(recipients)} recipient(s)."

