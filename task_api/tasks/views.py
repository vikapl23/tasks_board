from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Board, Comment, Task
from .permissions import IsOwnerOrReadOnly
from .serializers import BoardSerializer, CommentSerializer, TaskSerializer


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['id']


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('board', 'owner').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['board', 'status', 'owner']
    search_fields = ['title', 'board__name']
    ordering_fields = ['deadline', 'start_date']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        tasks = self.get_queryset().filter(deadline__lt=date.today()).exclude(status='done')
        return Response(self.get_serializer(tasks, many=True).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('task', 'owner').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['task', 'owner']
    search_fields = ['text']
    ordering_fields = ['created_at']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)