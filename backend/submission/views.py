from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated

from .models import Submission
from .serializers import SubmissionSerializer
from user.permissions import GetOnlyPermission

class SubmissionViewSet(ReadOnlyModelViewSet):
    """
    获取提交信息
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    # TODO: 提交信息的查看权限问题
    permission_classes = (GetOnlyPermission,)

class SubmitView(APIView):
    """
    提交
    """
    permission_classes = (IsAuthenticated,)
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                name='problem',
                required=True,
                location='form',
                schema=coreschema.Integer(
                    title='problem',
                    description='要提交的题目ID'
                )
            ),
            coreapi.Field(
                name='files',
                required=True,
                location='form',
                schema=coreschema.Array(
                    title='files',
                    items=coreschema.Integer,
                    description='要提交的文件（代码等）'
                )
            ),
        ]
    )
    def post(self, request, *args):
        # TODO: 提交评测功能
        return Response('TODO', status.HTTP_500_INTERNAL_SERVER_ERROR)