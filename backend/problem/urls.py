from django.urls import path, include
from rest_framework import routers
from .views import ProblemViewSet, TestCaseViewSet

router = routers.DefaultRouter()
router.register('problems', ProblemViewSet)
router.register('problem-testcases', TestCaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]