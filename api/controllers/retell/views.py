from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import create_web_call, handle_webhook

from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def create_web_call_view(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        name = body.get("name")
        company_email = body.get("company_email")
        phone = body.get("phone")
        industry = body.get("industry")

        # basic validation
        if not (name and company_email and phone and industry):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        call_data = create_web_call(
            name=name,
            company_email=company_email,
            phone=phone,
            industry=industry,
        )

        return JsonResponse(call_data, status=200)

    except Exception as e:
        logger.exception("Error creating web call")
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def retell_webhook_view(request):
    try:
        result = handle_webhook(request.data)
        # result will be "Event ignored", "Lead created", or "Lead updated"
        return Response({"detail": result}, status=status.HTTP_200_OK)
    except ValueError as e:
        # truly bad payload
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # log internally if you want
        logger.exception("Error in retell webhook")
        return Response({"error": "Internal webhook error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
