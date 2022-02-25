from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend


from .models import Comment, Topic
from .serializers import CommentSerializer, TopicSerializer

class TopicView(APIView):
    "提交Topic"
    
    def post(self, request, *args):
        self.check_permissions(request)
        data = request.data.copy()
        data['creator'] = request.user.id
        serializer = TopicSerializer(data=data)

        try: 
            serializer.is_valid(True)
            topic = serializer.save()
            print(serializer.data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopicViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    Topic view
    """
    queryset = Topic.objects.all().order_by('-update_time')
    serializer_class = TopicSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id','creator', "problem")

class CommentView(APIView):
    def post(self, request, *args):
        self.check_permissions(request)
        data = request.data.copy()
        data['replyer'] = request.user.id
        serializer = CommentSerializer(data=data)

        try: 
            serializer.is_valid(True)
            comment = serializer.save()
            print(serializer.data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    Topic view
    """
    queryset = Comment.objects.all().order_by('update_time')
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id','replyer', "topic")
