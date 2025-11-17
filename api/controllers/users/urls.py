from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_users_view, name="list_users"),
]
