from rest_framework import serializers
from .models import Submission, SubmissionResult
from problem.serializers import ProblemSerializer, ProblemListSerializer
from user.serializers import UserSerializer, UserPublicSerializer, UserPublicListSerializer

class SubmissionResultSerializer(serializers.ModelSerializer):
    result = serializers.CharField(source='get_result', read_only=True)
    
    class Meta:
        model = SubmissionResult
        fields = '__all__'
        #exclude = ['id', 'submission']

class SubmissionResultPublicSerializer(serializers.ModelSerializer):
    result = serializers.CharField(source='get_result', read_only=True)
    
    class Meta:
        model = SubmissionResult
        #fields = '__all__'
        exclude = ['app_data', 'log']

class SubmissionSerializer(serializers.ModelSerializer):
    problem_belong = ProblemSerializer(source='problem', read_only=True)
    user_belong = UserSerializer(source='user', read_only=True)
    
    results = SubmissionResultSerializer(source='get_results', read_only=True, many=True)
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    # judged = serializers.BooleanField(source='have_judged', read_only=True)
    # ac = serializers.BooleanField(source='is_ac', read_only=True)
    result = serializers.CharField(source='get_result', read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionPublicListSerializer(serializers.ModelSerializer):
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    result = serializers.CharField(source='get_result', read_only=True)

    problem_belong = ProblemListSerializer(source='problem', read_only=True)
    user_belong = UserPublicListSerializer(source='user', read_only=True)
    class Meta:
        model = Submission
        # fields = '__all__'
        exclude = ['submit_files']

class SubmissionPublicSerializer(serializers.ModelSerializer):
    problem_belong = ProblemSerializer(source='problem', read_only=True)
    user_belong = UserPublicSerializer(source='user', read_only=True)
    
    results = SubmissionResultPublicSerializer(source='get_results', read_only=True, many=True)
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    # judged = serializers.BooleanField(source='have_judged', read_only=True)
    # ac = serializers.BooleanField(source='is_ac', read_only=True)
    result = serializers.CharField(source='get_result', read_only=True)
    
    class Meta:
        model = Submission
        # fields = '__all__'
        exclude = ['submit_files']