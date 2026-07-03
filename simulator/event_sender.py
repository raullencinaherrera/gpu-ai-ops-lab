import os
import requests
from datetime import datetime, timezone

EVENT_PROCESSOR_URL = os.getenv(
    "EVENT_PROCESSOR_URL",
    "http://localhost:8080/events"
)


def send_event(event: dict) -> None:
    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    try:
        response = requests.post(EVENT_PROCESSOR_URL, json=event, timeout=5)
        response.raise_for_status()
        print(f"Event sent to ai-event-processor: {response.status_code}")
    except Exception as exc:
        print(f"Could not send event: {exc}")
