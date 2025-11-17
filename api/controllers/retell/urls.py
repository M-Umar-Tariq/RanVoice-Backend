from django.urls import path
from . import views

urlpatterns = [
    path("create-web-call/", views.create_web_call_view, name="create_web_call"),
    # path("webhook/", views.retell_webhook_view, name="retell_webhook"),
    path("webhook", views.retell_webhook_view),
]
