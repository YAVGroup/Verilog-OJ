from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import BasePermission

import django.contrib.auth.models

class JudgerAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # A header named X-JudgerSecret
        # ref: https://docs.djangoproject.com/en/3.0/ref/request-response/
        secret = request.META.get('HTTP_X_JUDGERSECRET')
        if not secret:
            return None

        if secret != settings.JUDGER_SECRET:
            return None

        # TODO: Test if IP in whitelist
        if request.META.get('REMOTE_ADDR') not in settings.JUDGER_IP_WHITELIST:
            print("Disallowed due to IP Whitelist policy.")
            return None

        # Fix user, since most scenario requires non-null user
        return (django.contrib.auth.models.AnonymousUser(), 'Judger')

class IsJudger(BasePermission):
    """
    Allow access from judgers
    """

    def has_permission(self, request, view):
        return bool(request.auth == 'Judger')