from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from judge.tasks import do_judge_task


from .models import Submission, SubmissionResult
from .serializers import SubmissionSerializer, SubmissionResultSerializer
from user.permissions import GetOnlyPermission
from judge.judger_auth import IsJudger
from problem.models import Problem

class SubmissionViewSet(ReadOnlyModelViewSet):
    """
    获取提交信息
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    # TODO: 提交信息的查看权限问题
    permission_classes = (GetOnlyPermission,)

# Read-only for users, allow to create for other users
class SubmissionResultViewSet(ModelViewSet):
    """
    Get submission result information
    """
    queryset = SubmissionResult.objects.all()
    serializer_class = SubmissionResultSerializer
    # TODO: 提交信息的查看权限问题
    permission_classes = (GetOnlyPermission | IsJudger,)


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
        serializer = SubmissionSerializer(data=request.data)
        # put the user segment in, ref: BaseSerializer docstring
        serializer.initial_data['user'] = request.user.id
        try:
            serializer.is_valid(True)
            subm = serializer.save()

            # Instantiate judge task for all testcases
            # Get all test cases related to this problem
            prob_id = serializer.data['problem']
            subm_id = subm.id
            print("{} {}".format(prob_id, subm_id))
            prob = Problem.objects.filter(id=prob_id)[0]
            for case in prob.get_testcases():
                do_judge_task.delay(subm_id, case.id)

            #do_judge_task(serializer.data['id'], serializer.data[''])
            return Response('提交评测', status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)