from rest_framework import serializers
from .models import Topic, Comment
from problem.serializers import ProblemListSerializer
from user.serializers import UserPublicListSerializer

class TopicSerializer(serializers.ModelSerializer):
    problem_belong = ProblemListSerializer(source='problem', read_only=True)
    user_belong = UserPublicListSerializer(source='creator', read_only=True)
    comments = serializers.ListField(source='get_comments', read_only=True)

    class Meta:
        model = Topic
        
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        
        fields = '__all__'