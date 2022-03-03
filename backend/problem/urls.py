from django.urls import path, include
from rest_framework import routers
from .views import ProblemView,ProblemViewSet, TestCaseViewSet, ProblemBookViewSet

router = routers.DefaultRouter()
router.register('problems', ProblemViewSet)
router.register('problem-testcases', TestCaseViewSet)
router.register('problem-books', ProblemBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('addproblem', ProblemView.as_view()),
]