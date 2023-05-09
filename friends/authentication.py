from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from friends.models import CustomUser


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user, None
