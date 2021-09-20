from rest_framework import serializers
from .models import Problem, TestCase

# TODO: 题目的创建者第一次设置后就不能更改了

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        #exclude = ['id', 'problem']
        fields = '__all__'

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'logic_id', 'name', 'create_time', 'deadline_time', 'level', 'tags']

class ProblemAdvancedListSerializer(serializers.ModelSerializer):
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    submitted_users = serializers.ListField(source='get_submitted_users', read_only=True)
    ac_users = serializers.ListField(source='get_ac_users', read_only=True)
    class Meta:
        model = Problem
        fields = ['id', 'logic_id', 'name', 'create_time', 'deadline_time', 'level', 'tags',
            'total_grade', 'submitted_users', 'ac_users']

class ProblemSerializer(serializers.ModelSerializer):
    testcases = TestCaseSerializer(source='get_testcases', read_only=True, many=True)
    total_grade = serializers.IntegerField(source='get_total_grade', read_only=True)
    submitted_users = serializers.ListField(source='get_submitted_users', read_only=True)
    ac_users = serializers.ListField(source='get_ac_users', read_only=True)
    # No need to provide submissions here
    # submissions = serializers.ListField(source='get_submissions', read_only=True)
    
    class Meta:
        model = Problem
        fields = '__all__'
        # read_only_fields = ('creater',)