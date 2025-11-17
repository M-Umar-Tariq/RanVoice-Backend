from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("retell/", include("api.controllers.retell.urls")),
    path("users/", include("api.controllers.users.urls")),
]
