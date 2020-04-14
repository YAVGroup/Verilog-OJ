from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer

# TODO: 重做文件管理接口

class FileViewSet(ModelViewSet):
    """
    文件管理(TODO)
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer