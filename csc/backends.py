from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password

class CSCBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            pwd_exists = user.password
            if pwd_exists:
                pwd_valid = check_password(password, pwd_exists)
                if pwd_valid:
                    return user

        except:
            pass
        return None