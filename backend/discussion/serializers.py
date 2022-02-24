from rest_framework import serializers
from .models import Topic, Comment

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        
        fields = '__all__'