from django.contrib.auth.backends import BaseBackend

class SSOBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        pass