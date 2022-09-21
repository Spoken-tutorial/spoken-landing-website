from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from spokenlogin.models import SpokenUser
from django.contrib.auth.hashers import check_password

class SpokenBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            sp_user = SpokenUser.objects.get(username=username)
            pwd_valid = check_password(password, sp_user.password)
            if pwd_valid:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email=username)
                    except User.DoesNotExist:
                        user = User(username=sp_user.username)
                        user.email = sp_user.email
                        user.first_name = sp_user.first_name
                        user.last_name = sp_user.last_name
                        user.is_active = True
                        user.save()
                return user
        except SpokenUser.DoesNotExist:
             return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None