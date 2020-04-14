from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Problem, TestCase
from .serializers import ProblemSerializer, TestCaseSerializer
from user import permissions

class ProblemViewSet(ModelViewSet):
    """
    获取和修改题目信息
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (permissions.GetOnlyPermission,)

class TestCaseViewSet(ModelViewSet):
    """
    获取和修改测试点信息
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = (permissions.GetOnlyPermission,)