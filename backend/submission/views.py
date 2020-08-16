from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from judge.tasks import do_judge_task

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Submission, SubmissionResult
from .serializers import SubmissionSerializer, SubmissionResultSerializer
from .serializers import SubmissionPublicSerializer, SubmissionResultPublicSerializer
from user.permissions import GetOnlyPermission
from judge.judger_auth import IsJudger
from problem.models import Problem

class SubmissionViewSet(ReadOnlyModelViewSet):
    """
    获取提交信息
    """
    queryset = Submission.objects.all()
    #serializer_class = SubmissionSerializer
    # TODO: 提交信息的查看权限问题
    permission_classes = (GetOnlyPermission,)

    def get_serializer_class(self):
        """
        Override parent code from rest_framework.generics.GenericAPIView
        to dynamically adjust the item to be used
        """
        if not hasattr(self.request, 'user'): # 生成文档用
            return SubmissionSerializer
        elif self.request.auth == "Judger" or self.request.user.is_superuser:
            return SubmissionSerializer
        elif self.request.method == 'GET' and (not 'pk' in self.kwargs):
            # Check if we're querying a specific one
            # In list mode, the log and app_data is always hidden
            return SubmissionPublicSerializer
        elif self.request.method == 'GET' and 'pk' in self.kwargs:
            # In retrive mode
            user_id = self.request.user.id
            if user_id is None:
                return SubmissionPublicSerializer
            else:
                subm = Submission.objects.filter(id=self.request.data['submission'])[0]
                if str(subm.user.id) != user_id:
                    return SubmissionPublicSerializer
                else:
                    return SubmissionSerializer
        else:
            return SubmissionSerializer

# Read-only for users, allow to create for other users
class SubmissionResultViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):
    """
    Get submission result information
    """
    queryset = SubmissionResult.objects.all()
    #serializer_class = SubmissionResultSerializer
    # TODO: 提交信息的查看权限问题
    permission_classes = (GetOnlyPermission | IsJudger,)

    def get_serializer_class(self):
        """
        Override parent code from rest_framework.generics.GenericAPIView
        to dynamically adjust the item to be used
        """
        if not hasattr(self.request, 'user'): # 生成文档用
            return SubmissionResultSerializer
        elif self.request.auth == "Judger" or self.request.user.is_superuser:
            return SubmissionResultSerializer
        elif self.request.method == 'GET' and (not 'pk' in self.kwargs):
            # Check if we're querying a specific one
            # In list mode, the log and app_data is always hidden
            return SubmissionResultPublicSerializer
        elif self.request.method == 'GET' and 'pk' in self.kwargs:
            # In retrive mode
            user_id = self.request.user.id
            if user_id is None:
                return SubmissionResultPublicSerializer
            else:
                subm = Submission.objects.filter(id=self.request.data['submission'])[0]
                if str(subm.user.id) != user_id:
                    return SubmissionResultPublicSerializer
                else:
                    return SubmissionResultSerializer
        else:
            return SubmissionResultSerializer

class SubmitView(APIView):
    """
    提交
    """
    permission_classes = (IsAuthenticated,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(name='problem',
                      required=True,
                      location='form',
                      schema=coreschema.Integer(title='problem',
                                                description='要提交的题目ID')),
        coreapi.Field(name='submit_files',
                      required=True,
                      location='form',
                      schema=coreschema.Array(title='submit_files',
                                              items=coreschema.Integer,
                                              description='要提交的文件（代码等）')),
    ])

    def post(self, request, *args):
        # Fix bug: must check permission first
        self.check_permissions(request)

        # put the user segment in, ref: BaseSerializer docstring
        # Fix bug: AttributeError: This QueryDict instance is immutable
        # ref: https://stackoverflow.com/questions/44717442/this-querydict-instance-is-immutable
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = SubmissionSerializer(data=data)

        # print(request.data)
        # print(serializer.initial_data)
        try:
            serializer.is_valid(True)
            subm = serializer.save()

            # Instantiate judge task for all testcases
            # Get all test cases related to this problem
            prob_id = serializer.data['problem']
            subm_id = subm.id
            # print("{} {}".format(prob_id, subm_id))
            prob = Problem.objects.filter(id=prob_id).first()
            if prob == None:
                return Response('No such problem', status.HTTP_404_NOT_FOUND)

            for case in prob.get_testcases():
                # Create a new SubmissionResult structure
                subm_res = SubmissionResult.objects.create(
                    status='PENDING',
                    submission=subm,
                    testcase=case,
                    grade=0,
                    log="",
                    app_data="",
                    possible_failure='NA'
                )

                do_judge_task.delay(subm_id, case.id, subm_res.id)

            #do_judge_task(serializer.data['id'], serializer.data[''])
            return Response(serializer._data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)