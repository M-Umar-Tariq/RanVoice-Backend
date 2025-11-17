from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.serializers.user_info_serializers import UserInfoSerializer
from .services import get_all_users

@api_view(["GET"])
def list_users_view(request):
    users = get_all_users()
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
