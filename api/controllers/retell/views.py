from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import create_web_call, handle_webhook

@api_view(["POST"])
def create_web_call_view(request):
    try:
        data = create_web_call()
        return Response(data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except RuntimeError as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception:
        return Response({"error": "Unexpected server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def retell_webhook_view(request):
    try:
        handle_webhook(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
