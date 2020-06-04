from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
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

from django.shortcuts import render, redirect
import sys
sys.path.append('../')
from cas_client import CASClient
import random

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
    # {"username":"test", "password":"test1234"}
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
            # ticket = request.COOKIES.get('ticket')
            rep = Response('logout succeed')
            # if ticket:
            #     rep.delete_cookie('ticket')
            return rep
        else:
            return Response('not login yet')

class UserUSTCLoginView(APIView):
    """
    通过USTC统一身份认证登录，用法：在登陆时通过一个按钮之类的东西拉起http://127.0.0.1:8000/api/user/ustc-login页面，
    会自动跳转到USTC统一身份认证界面，登陆成功返回ustc-login页面，并且返回一个service ticket用于用户验证。如果验证
    时发现服务器端没有响应，返回HTTP_503_SERVICE_UNAVAILABLE；否则返回HTTP_200_OK。
    注：返回值只是暂定，后期根据需求来改
    """
    def get(self, request, *args):
        # 统一身份认证登录
        ticket = request.GET.get('ticket')
        cas_url = 'https://passport.ustc.edu.cn'
        app_login_url = 'http://home.ustc.edu.cn/~zkdliushuo'
        cas_client = CASClient(cas_url, auth_prefix='')
        if ticket:
            try:
                cas_response = cas_client.perform_service_validate(
                    ticket=ticket,
                    service_url=app_login_url,
                )
            except Exception:
                # CAS server is currently broken, try again later.
                return Response('CAS server is currently broken, try again later.', status.HTTP_503_SERVICE_UNAVAILABLE)
            if cas_response and cas_response.success:
                student_id = cas_response.user
                try:
                    # 已经有用户使用该学号注册过账户了
                    user = User.objects.get(student_id=student_id)
                    login(request, user)
                except:
                    # 没有人用该学号注册账户, 默认使用科大邮箱用户名作为用户名，密码设置为学号，否则随机生成字符串作为用户名
                    email = cas_response.data.get('attributes').get('email')
                    username = ''
                    i = 0
                    while True:
                        if email[i] == '@':
                            break
                        username += email[i]
                        i = i + 1
                    
                    while True:
                        try:
                            user = {'username':username, 'student_id':student_id, 'password':student_id}
                            serializer = UserSerializer(data=user)
                            serializer.is_valid(True)
                            serializer.save()
                            login(request, user)
                            break
                        except Exception:
                            username = ''
                            for i in range(0,10):
                                username += random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')

                rep = Response('OK', status.HTTP_200_OK)        # 更换为 rep = redirect('home')
                # rep.set_cookie("ticket", ticket)
                return rep
        cas_login_url = cas_client.get_login_url(service_url=app_login_url)
        return redirect(cas_login_url)

class UserSignupView(GenericAPIView):
    """
    注册
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    def post(self, request, *args):
        # 注册
        try:
            data = request.data.copy()
            data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            serializer.is_valid(True)
            serializer.save()
            return Response('注册成功', status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
        
