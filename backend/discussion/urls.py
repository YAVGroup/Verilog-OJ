from django.urls import path, include
from rest_framework import routers
from .views import TopicViewSet, CommentViewSet, TopicView, CommentView

router = routers.DefaultRouter()
router.register('topic', TopicViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('addtopic', TopicView.as_view()),
    path('addcomment', CommentView.as_view()),
]