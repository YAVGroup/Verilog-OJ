from .models import News
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #exclude = ['id', 'problem']
        fields = '__all__'
