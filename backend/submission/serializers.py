from rest_framework import serializers
from .models import Submission, SubmissionResult
from problem.serializers import ProblemSerializer
from user.serializers import UserSerializer, UserPublicSerializer

class SubmissionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionResult
        fields = '__all__'
        #exclude = ['id', 'submission']

class SubmissionResultPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionResult
        #fields = '__all__'
        exclude = ['app_data', 'log']

class SubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    user = UserSerializer()
    
    results = SubmissionResultSerializer(source='get_results', read_only=True, many=True)
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    judged = serializers.BooleanField(source='have_judged', read_only=True)
    ac = serializers.BooleanField(source='is_ac', read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionPublicSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    user = UserPublicSerializer()
    
    results = SubmissionResultPublicSerializer(source='get_results', read_only=True, many=True)
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    judged = serializers.BooleanField(source='have_judged', read_only=True)
    ac = serializers.BooleanField(source='is_ac', read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'