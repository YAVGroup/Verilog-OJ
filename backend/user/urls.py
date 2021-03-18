from django.conf.urls import url,include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
routers.register('users', views.UserViewSet)

urlpatterns = [
    url('', include(routers.urls)),
    url('user/login', views.UserLoginView.as_view()),
    url('user/logout', views.UserLogoutView.as_view()),
    url('user/ustc-login', views.UserUSTCLoginView.as_view(), name='ustc-login-view'),
    url('user/signup', views.UserSignupView.as_view()),
    url('user/status-login', views.UserLoginStatusView.as_view())
]