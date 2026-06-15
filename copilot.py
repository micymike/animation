import requests
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

DIRECT_LINE_SECRET = os.getenv("DIRECT_LINE_SECRET", "").strip().strip('"').strip("'")
DIRECT_LINE_REGION = os.getenv("DIRECT_LINE_REGION", "").strip().strip('"').strip("'")
REQUEST_TIMEOUT = 30


def _base_url():
    r = DIRECT_LINE_REGION
    if r:
        return f"https://{r}.directline.botframework.com/v3/directline"
    return "https://directline.botframework.com/v3/directline"


class CopilotError(RuntimeError):
    pass


def _check_response(response: requests.Response) -> None:
    if response.ok:
        return
    try:
        body = response.json()
        err = body.get("error", {})
        code = err.get("code", "")
        message = err.get("message", "")
    except ValueError:
        code = ""
        message = response.text[:200]
    detail = f"{code}: {message}" if code else message or response.reason
    raise CopilotError(f"Direct Line HTTP {response.status_code}. {detail}")


def _auth_header(secret_or_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {secret_or_token}"}


def _generate_token() -> str:
    res = requests.post(
        f"{_base_url()}/tokens/generate",
        headers=_auth_header(DIRECT_LINE_SECRET),
        timeout=REQUEST_TIMEOUT,
    )
    _check_response(res)
    return res.json()["token"]


def start_conversation():
    if not DIRECT_LINE_SECRET:
        raise CopilotError("DIRECT_LINE_SECRET missing in .env")
    token = _generate_token()
    res = requests.post(
        f"{_base_url()}/conversations",
        headers=_auth_header(token),
        timeout=REQUEST_TIMEOUT,
    )
    _check_response(res)
    data = res.json()
    return data["conversationId"], data["token"]


def _get_activities(conversation_id: str, token: str, watermark: str | None = None) -> dict:
    headers = {**_auth_header(token), "Content-Type": "application/json"}
    url = f"{_base_url()}/conversations/{conversation_id}/activities"
    if watermark:
        url = f"{url}?watermark={watermark}"

    res = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    _check_response(res)
    return res.json()


def send_message(conversation_id: str, token: str, text: str) -> str:
    headers = {**_auth_header(token), "Content-Type": "application/json"}
    before = _get_activities(conversation_id, token)
    watermark = before.get("watermark")

    payload = {"type": "message", "from": {"id": "user"}, "text": text}
    res = requests.post(
        f"{_base_url()}/conversations/{conversation_id}/activities",
        headers=headers, json=payload, timeout=REQUEST_TIMEOUT,
    )
    _check_response(res)

    for _ in range(10):
        time.sleep(1)
        data = _get_activities(conversation_id, token, watermark)
        watermark = data.get("watermark", watermark)
        activities = data.get("activities", [])
        replies = [
            a for a in activities
            if a.get("from", {}).get("role") == "bot" and a.get("type") == "message" and a.get("text")
        ]
        if replies:
            return replies[-1]["text"]
    return "No response from Copilot."
