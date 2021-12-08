from django.http import FileResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from user.permissions import IsAdminUser
from judge.judger_auth import IsJudger

from .models import File
from .serializers import FileSerializer
from .permissions import  IsOwnerOrReadOnly


class FileViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """
    文件管理
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # permission_classes = (IsOwnerOrReadOnly | IsJudger,)

    # permission_classes = [IsOwnerOrReadOnly | IsJudger, ] 

    
    def retrieve(self, request, *args, **kwargs):
        # 重写了GET文件，此时可以直接
        self.permission_classes = (  IsOwnerOrReadOnly | IsJudger | IsAdminUser,)

        instance = self.get_object()        
        file_handle = instance.file.open()
        response = FileResponse(file_handle)
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.name

        return response
    
    def list(self, request, *args, **kwargs):
        # Standard bitwise operator have been overloaded in permission classes
        # ref: https://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy
        self.permission_classes = (IsAdminUser | IsJudger,)
        #print("{} {}".format(request.user, request.auth))
        self.check_permissions(request)
        
        return super(FileViewSet, self).list(self, request, args, kwargs)