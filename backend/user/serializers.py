#from django.contrib.validators import UnicodeUsernameValidator
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

# 给出全部用户信息
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'groups', 'user_permissions'] # 这些字段现在暂时用不上

# 仅给出用户对外界公开的信息
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_active', 'is_mail_authenticated', 'groups', 'user_permissions']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('username or password is wrong')
        return {'user': user}