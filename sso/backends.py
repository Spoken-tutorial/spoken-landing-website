from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .views import prepare_django_request, init_saml_auth
from .models import NasscomUser

class SSOBackend(ModelBackend):

    def authenticate(self, request, auth=None):
        if auth.is_authenticated():
            username = request.session['samlNameId']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, email=username)
                user.save()
                NasscomUser.objects.create(user=user)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None