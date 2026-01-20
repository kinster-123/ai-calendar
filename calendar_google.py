from __future__ import print_function
from datetime import timedelta
import os.path

import httplib2
import socks
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 权限：读写日历
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    # token.json 会在第一次授权后自动生成
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 如果没有凭据 or 过期
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_console()

        # 保存 token
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def insert_event_to_google_calendar(event):
    service = get_calendar_service()

    start_time = event.start_time
    end_time = event.end_time or (start_time + timedelta(hours=1))

    event_body = {
        "summary": event.title,
        "location": event.location,
        "description": event.original_text,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Shanghai",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Shanghai",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    return created_event.get("htmlLink")
