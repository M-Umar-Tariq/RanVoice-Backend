from database.models.user_info import UserInfo

def get_all_users():
    return UserInfo.objects.all()
