from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import User
# from submission.serializers import SubmissionSerializer, SubmissionPublicSerializer
# from problem.serializers import ProblemSerializer

# 给出全部用户信息
class UserSerializer(serializers.ModelSerializer):
    # submissions = SubmissionSerializer(source='get_submissions', read_only=True, many=True)
    # submitted_problems = ProblemSerializer(source='get_submitted_problems', read_only=True, many=True)
    # ac_problems = ProblemSerializer(source='get_ac_problems', read_only=True, many=True)
    # total_score = serializers.IntegerField(source='get_total_score', read_only=True)
    submitted_problems = serializers.ListField(source='get_submitted_problems', read_only=True)
    ac_problems = serializers.ListField(source='get_ac_problems', read_only=True)
    total_score = serializers.IntegerField(source='get_total_score', read_only=True)
    undone_problems = serializers.ListField(source='get_undone_problems', read_only=True)


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        try:
            validate_password(validated_data['password'])
            validated_data['is_password_strong'] = True
        except ValidationError:
            validated_data['is_password_strong'] = False

        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        if validated_data.get('password') is not None:
            try:
                validate_password(validated_data['password'])
                validated_data['is_password_strong'] = True
            except ValidationError:
                validated_data['is_password_strong'] = False
            user.set_password(validated_data['password'])
            user.is_password_strong = validated_data['is_password_strong']
            user.save()

        return user

    # WARN: Serializer fields that are set without read-only can be updated on call to create/update.
    #       and some priviledge escalations can occur.
    # To avoid, use https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields
    # to set explicitly
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'groups', 'user_permissions'] # 这些字段现在暂时用不上，且暴露会给出 create/update 方法
        read_only_fields = ['is_superuser', 'is_mail_authenticated', 'student_id', 'date_joined', 'last_login', 'is_password_strong', 'id']


# 仅给出用户对外界公开的信息
class UserPublicSerializer(serializers.ModelSerializer):
    # submissions = SubmissionPublicSerializer(source='get_submissions', read_only=True, many=True)
    # submitted_problems = ProblemSerializer(source='get_submitted_problems', read_only=True, many=True)
    # ac_problems = ProblemSerializer(source='get_ac_problems', read_only=True, many=True)
    # total_score = serializers.IntegerField(source='get_total_score', read_only=True)
    submitted_problems = serializers.ListField(source='get_submitted_problems', read_only=True)
    ac_problems = serializers.ListField(source='get_ac_problems', read_only=True)
    total_score = serializers.IntegerField(source='get_total_score', read_only=True)
    undone_problems = serializers.ListField(source='get_undone_problems', read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_active', 'is_mail_authenticated', 'groups', 'user_permissions', 'is_password_strong']
        read_only_fields = ['is_superuser', 'is_mail_authenticated', 'student_id', 'date_joined', 'last_login', 'id']

class UserPublicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('username or password is wrong')
        return {'user': user}