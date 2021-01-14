"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url,include
from django.conf import settings
from django.views.static import serve
#from user.views import UserLoginView, UserLogoutView
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path(settings.WEBPATH_PREFIX, include(
        [
            path('admin-django/', admin.site.urls),
            url('docs/', include_docs_urls(title="接口文档", authentication_classes=[], permission_classes=[])),
            url('api/', include('user.urls')),
            url('api/', include('file.urls')),
            url('api/', include('problem.urls')),
            url('api/', include('submission.urls')),
            url('api/', include('news.urls'))
        ]
    ))
]

if settings.HOST_DJANGO_STATIC:
    # Temporary procedure. TODO: remove this and add into nginx
    urlpatterns += [
        # Works for r'^oj/static-django/(?P<path>.*)$'
        re_path(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT
        })
    ]

