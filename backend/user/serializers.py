from django.contrib.auth import authenticate
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

    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'groups', 'user_permissions'] # 这些字段现在暂时用不上

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
        exclude = ['password', 'is_staff', 'is_active', 'is_mail_authenticated', 'groups', 'user_permissions']

class UserPublicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('username or password is wrong')
        return {'user': user}