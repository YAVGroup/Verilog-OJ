from rest_framework.serializers import ModelSerializer
from .models import File

# TODO: 文件上传的时候自动生成UUID，并设置文件名和大小
# TODO: 进一步的文件管理，如区分属于不同题目或是提交的文件到不同的路径下

class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'