from rest_framework.viewsets import ModelViewSet

from .models import Problem, TestCase
from .serializers import ProblemSerializer, TestCaseSerializer, ProblemAdvancedListSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from user import permissions

class ProblemViewSet(ModelViewSet):
    """
    获取和修改题目信息
    """
    queryset = Problem.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id','owner', 'level')
    search_fields = ('name', 'level', 'tags')
    pagination_class = LimitOffsetPagination
    #serializer_class = ProblemSerializer

    def get_serializer_class(self):
        """
        Override parent code from rest_framework.generics.GenericAPIView
        to dynamically adjust the item to be used
        """
        if not hasattr(self.request, 'user'): # 生成文档用
            return ProblemSerializer
        elif self.request.method == 'GET' and (not 'pk' in self.kwargs):
            # Check if we're querying a specific one
            # In list mode, the log and app_data is always hidden
            return ProblemAdvancedListSerializer
        else:
            return ProblemSerializer

    permission_classes = (permissions.GetOnlyPermission,)

class TestCaseViewSet(ModelViewSet):
    """
    获取和修改测试点信息
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = (permissions.GetOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id','problem','type')