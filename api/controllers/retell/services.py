# import os
# import requests
# from database.models.user_info import UserInfo

# RETELL_API_URL = "https://api.retellai.com/v2/create-web-call"

# def create_web_call():
#     api_key = os.getenv("RETELL_API_KEY")
#     agent_id = os.getenv("RETELL_AGENT_ID")

#     if not api_key or not agent_id:
#         raise ValueError("RETELL_API_KEY or RETELL_AGENT_ID missing in environment")

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "agent_id": agent_id,
#         "metadata": {"source": "website_healthcare_qa"},
#     }

#     response = requests.post(RETELL_API_URL, json=payload, headers=headers)
#     try:
#         response.raise_for_status()
#     except requests.exceptions.HTTPError:
#         raise RuntimeError(f"Retell error {response.status_code}: {response.text}")

#     data = response.json()
#     access_token = data.get("access_token")
#     call_id = data.get("call_id")

#     if not access_token:
#         raise RuntimeError("Retell did not return access_token")

#     return {
#         "accessToken": access_token,
#         "callId": call_id,
#     }


# def handle_webhook(data):
#     event = data.get("event")
#     call = data.get("call")

#     if not event or not call:
#         return "Invalid webhook payload"

#     if event not in ["call_analyzed", "call_completed", "call.finished"]:
#         return "Event ignored"

#     call_id = call.get("call_id")
#     analysis = call.get("call_analysis", {})

#     name = age = gender = None

#     sources = [
#         analysis.get("custom_analysis_data"),
#         analysis.get("custom_defined_data"),
#         analysis.get("custom_data"),
#         analysis.get("data"),
#     ]

#     for src in sources:
#         if not src:
#             continue
#         name = name or src.get("name")
#         age = age or src.get("age")
#         gender = gender or src.get("gender")

#     profile = analysis.get("structured_data", {}).get("user_profile", {})
#     if profile:
#         name = name or profile.get("name")
#         age = age or profile.get("age")
#         gender = gender or profile.get("gender")

#     if name or age or gender:
#         UserInfo.objects.create(
#             name=name if name else None,
#             age=age if age else None,
#             gender=gender if gender else None,
#             call_id=call_id,
#         )

#     return "Processed"


import os
import requests
import logging

from database.models.user_info import UserInfo

logger = logging.getLogger(__name__)

RETELL_API_URL = "https://api.retellai.com/v2/create-web-call"


def create_web_call():
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
        "metadata": {"source": "ranvoice_website_voice_sales"},
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
    analysis = call.get("call_analysis", {}) or {}

    sources = [
        analysis.get("custom_analysis_data"),
        analysis.get("custom_defined_data"),
        analysis.get("custom_data"),
        analysis.get("data"),
    ]

    # Lead fields
    first_name = email = phone = business_name = None
    industry_type = monthly_call_volume = role = primary_pain_point = None
    time_preference = None
    intent = None
    lead_ready = None
    pain_intensity = None

    for src in sources:
        if not src:
            continue

        first_name = first_name or src.get("first_name")
        email = email or src.get("email")
        phone = phone or src.get("phone")
        business_name = business_name or src.get("business_name")

        industry_type = industry_type or src.get("industry_type")
        monthly_call_volume = monthly_call_volume or src.get("monthly_call_volume")
        role = role or src.get("role")
        primary_pain_point = primary_pain_point or src.get("primary_pain_point")
        time_preference = time_preference or src.get("time_preference")

        intent = intent or src.get("intent")
        pain_intensity = pain_intensity or src.get("pain_intensity")

        if lead_ready is None and "lead_ready" in src:
            lr = src.get("lead_ready")
            if isinstance(lr, bool):
                lead_ready = lr
            elif isinstance(lr, str):
                lead_ready = lr.lower() in ["true", "1", "yes"]

   
    obj, created = UserInfo.objects.update_or_create(
        call_id=call_id,
        defaults={
            "first_name": first_name,
            "email": email,
            "phone": phone,
            "business_name": business_name,
            "industry_type": industry_type,
            "monthly_call_volume": monthly_call_volume,
            "role": role,
            "primary_pain_point": primary_pain_point,
            "time_preference": time_preference,
            "intent": intent or "lead",
            "lead_ready": lead_ready,
            "pain_intensity": pain_intensity,
            "raw_payload": data,
        },
    )

    return "Lead created" if created else "Lead updated"
