from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin

from .models import Problem, TestCase, ProblemBook
from .serializers import ProblemSerializer, TestCaseSerializer, ProblemAdvancedListSerializer, ProblemBookSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user import permissions

class ProblemView(APIView):
    "提交题目"
    permission_classes = (IsAdminUser,)
    
    def post(self, request, *args):
        self.check_permissions(request)
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = ProblemSerializer(data=data)

        try: 
            serializer.is_valid(True)
            problem = serializer.save()
            print(serializer.data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProblemViewSet(ModelViewSet):
    """
    获取和修改题目信息
    """
    queryset = Problem.objects.all().order_by('logic_id')

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id','logic_id','owner', 'level')
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

class ProblemBookViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = ProblemBook.objects.all()
    serializer_class = ProblemBookSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'owner', 'sequence_id')
