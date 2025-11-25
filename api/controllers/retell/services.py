import os
import requests
import logging

from django.utils.dateparse import parse_datetime
from database.models.user_info import UserInfo

logger = logging.getLogger(__name__)

RETELL_API_URL = "https://api.retellai.com/v2/create-web-call"


def create_web_call(name: str, company_email: str, phone: str, industry: str):
    api_key = os.getenv("RETELL_API_KEY")
    agent_id = os.getenv("RETELL_AGENT_ID")

    if not api_key or not agent_id:
        raise ValueError("RETELL_API_KEY or RETELL_AGENT_ID missing in environment")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "agent_id": agent_id,

        # ✅ Hard 2-minute stop
        "agent_override": {
            "agent": {
                "max_call_duration_ms": 120000,
            }
        },

        # 🔹 Injected into LLM prompt
        "retell_llm_dynamic_variables": {
            "name": str(name),
            "company_email": str(company_email),
            "phone": str(phone),
            "industry": str(industry),
        },

        # 🔹 For webhook + DB
        "metadata": {
            "source": "ranvoice_website_voice_sales",
            "name": name,
            "company_email": company_email,
            "phone": phone,
            "industry": industry,
        },

        "custom_data": {
            "name": name,
            "company_email": company_email,
            "phone": phone,
            "industry": industry,
        },
    }

    response = requests.post(RETELL_API_URL, json=payload, headers=headers)

    try:
        response.raise_for_status()
    except Exception:
        logger.error("Retell create web call failed: %s", response.text)
        raise RuntimeError(f"Retell error {response.status_code}: {response.text}")

    data = response.json()

    return {
        "accessToken": data.get("access_token"),
        "callId": data.get("call_id"),
    }


def handle_webhook(data: dict):

    event = data.get("event") or data.get("event_type")
    call = data.get("call")

    if not event or not call:
        raise ValueError("Invalid webhook payload")

    if event != "call_analyzed":
        return "Event ignored"

    call_id = call.get("call_id")
    if not call_id:
        raise ValueError("Missing call_id in webhook payload")

    analysis = call.get("call_analysis", {}) or {}

    transcript = (
        analysis.get("transcript")
        or call.get("transcript")
        or None
    )

    # 🔹 Sources Retell may fill
    sources = [
        analysis.get("custom_analysis_data"),
        analysis.get("custom_defined_data"),
        analysis.get("custom_data"),
        analysis.get("data"),
        call.get("metadata"),
        call.get("custom_data"),
    ]

    name = company_email = phone = None
    industry = None

    for src in sources:
        if not src:
            continue

        name = name or src.get("name")
        company_email = company_email or src.get("company_email")
        phone = phone or src.get("phone")
        industry = industry or src.get("industry") or src.get("industry_type")

    # 🔹 Save clean lead
    obj, created = UserInfo.objects.update_or_create(
        call_id=call_id,
        defaults={
            "name": name,            
            "company_email": company_email,        
            "phone": phone,
            "industry_type": industry,
            "transcript": transcript,
            "raw_payload": data,
        },
    )

    return "Lead created" if created else "Lead updated"
