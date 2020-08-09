from django.http import FileResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser

from .models import File
from .serializers import FileSerializer

class FileViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """
    文件管理
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # 重写了GET文件，此时可以直接
        instance = self.get_object()
        file_handle = instance.file.open()
        response = FileResponse(file_handle)
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.name
        return response
    
    # def list(self, request, *args, **kwargs):
    #     self.permission_classes = (IsAdminUser,)
    #     self.check_permissions(request)
    #     super(FileViewSet, self).list(self, request, args, kwargs)