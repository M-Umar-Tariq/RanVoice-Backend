# import os
# import requests
# import logging

# from database.models.user_info import UserInfo

# logger = logging.getLogger(__name__)

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
#         "metadata": {"source": "ranvoice_website_voice_sales"},
#     }

#     response = requests.post(RETELL_API_URL, json=payload, headers=headers)

#     try:
#         response.raise_for_status()
#     except Exception:
#         logger.error("Retell create web call failed: %s", response.text)
#         raise RuntimeError(f"Retell error {response.status_code}: {response.text}")

#     data = response.json()

#     return {
#         "accessToken": data.get("access_token"),
#         "callId": data.get("call_id"),
#     }


# def handle_webhook(data: dict):
#     event = data.get("event") or data.get("event_type")
#     call = data.get("call")

#     if not event or not call:
#         raise ValueError("Invalid webhook payload")

#     if event != "call_analyzed":
#         return "Event ignored"

#     call_id = call.get("call_id")
#     analysis = call.get("call_analysis", {}) or {}

#     sources = [
#         analysis.get("custom_analysis_data"),
#         analysis.get("custom_defined_data"),
#         analysis.get("custom_data"),
#         analysis.get("data"),
#     ]

#     # Lead fields
#     first_name = email = phone = business_name = None
#     industry_type = monthly_call_volume = role = primary_pain_point = None
#     time_preference = None
#     intent = None
#     lead_ready = None
#     pain_intensity = None

#     for src in sources:
#         if not src:
#             continue

#         first_name = first_name or src.get("first_name")
#         email = email or src.get("email")
#         phone = phone or src.get("phone")
#         business_name = business_name or src.get("business_name")

#         industry_type = industry_type or src.get("industry_type")
#         monthly_call_volume = monthly_call_volume or src.get("monthly_call_volume")
#         role = role or src.get("role")
#         primary_pain_point = primary_pain_point or src.get("primary_pain_point")
#         time_preference = time_preference or src.get("time_preference")

#         intent = intent or src.get("intent")
#         pain_intensity = pain_intensity or src.get("pain_intensity")

#         if lead_ready is None and "lead_ready" in src:
#             lr = src.get("lead_ready")
#             if isinstance(lr, bool):
#                 lead_ready = lr
#             elif isinstance(lr, str):
#                 lead_ready = lr.lower() in ["true", "1", "yes"]

   
#     obj, created = UserInfo.objects.update_or_create(
#         call_id=call_id,
#         defaults={
#             "first_name": first_name,
#             "email": email,
#             "phone": phone,
#             "business_name": business_name,
#             "industry_type": industry_type,
#             "monthly_call_volume": monthly_call_volume,
#             "role": role,
#             "primary_pain_point": primary_pain_point,
#             "time_preference": time_preference,
#             "intent": intent or "lead",
#             "lead_ready": lead_ready,
#             "pain_intensity": pain_intensity,
#             "raw_payload": data,
#         },
#     )

#     return "Lead created" if created else "Lead updated"











import os
import requests
import logging

from django.utils.dateparse import parse_datetime

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
    if not call_id:
        raise ValueError("Missing call_id in webhook payload")

    analysis = call.get("call_analysis", {}) or {}


    sources = [
        analysis.get("custom_analysis_data"),
        analysis.get("custom_defined_data"),
        analysis.get("custom_data"),
        analysis.get("data"),
    ]


    first_name = email = phone = business_name = None
    industry_type = monthly_call_volume = role = primary_pain_point = None
    appointment_time = None
    their_problem = None

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

        their_problem = their_problem or src.get("their_problem")

        if appointment_time is None:
            appt_raw = src.get("appointment_time")
            if isinstance(appt_raw, str):
                parsed = parse_datetime(appt_raw)
                if parsed is not None:
                    appointment_time = parsed


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
            "appointment_time": appointment_time,
            "their_problem": their_problem,
            "raw_payload": data,
        },
    )

    return "Lead created" if created else "Lead updated"
