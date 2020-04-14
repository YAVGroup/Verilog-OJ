from django.shortcuts import render
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import UserSerializer, UserPublicSerializer, UserLoginSerializer
from .permissions import GetOnlyPermission, OthersGetOnlyPermission

class UserViewSet(ModelViewSet):
    """
    获取和修改用户信息（create仅限管理员，update/partial_update/delete仅限管理员和本人）
    """
    # permission_classes = (permissions.OthersGetOnlyPermission,)
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if not hasattr(self.request, 'user'): # 生成文档用
            return UserSerializer
        elif self.request.user.is_superuser:
            return UserSerializer
        elif self.request.method == 'GET' and ((not 'pk' in self.kwargs) or str(self.request.user.id) != self.kwargs['pk']):
            return UserPublicSerializer
        else:
            return UserSerializer
    
    def get_permissions(self):
        if 'pk' in self.kwargs:
            return [OthersGetOnlyPermission()]
        else:
            return [GetOnlyPermission()]

class UserLoginView(APIView):
    """
    通过用户名和密码进行登录
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                name='username',
                required=True,
                location='form',
                schema=coreschema.String(
                    title='username',
                    description='用户名'
                )
            ),
            coreapi.Field(
                name='password',
                required=True,
                location='form',
                schema=coreschema.String(
                    title='password',
                    description='密码'
                )
            ),
        ]
    )
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data)

class UserLogoutView(APIView):
    """
    用户登出
    """
    def get(self, request, *args):
        if request.user.id:
            logout(request)
            return Response('logout succeed')
        else:
            return Response('not login yet')

class UserUSTCLoginView(APIView):
    """
    通过USTC统一身份认证登录(TODO)
    """
    def post(self,request, *args):
        # TODO: 统一身份认证登录
        return Response('TODO', status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSignupView(GenericAPIView):
    """
    注册(TODO)
    """
    serializer_class = UserSerializer
    def post(self, request, *args):
        # TODO: 注册
        return Response('TODO', status.HTTP_500_INTERNAL_SERVER_ERROR)
        