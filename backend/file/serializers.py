from rest_framework.serializers import ModelSerializer
from .models import File

class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
    
    def to_representation(self, obj):
        ret = super(FileSerializer, self).to_representation(obj)
        ret.pop('file')
        return ret