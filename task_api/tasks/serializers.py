from datetime import date

from rest_framework import serializers

from .models import Board, Task


class TaskSerializer(serializers.ModelSerializer):
    board = serializers.StringRelatedField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'board', 'status', 'deadline', 'is_overdue']

    def get_is_overdue(self, obj):
        return obj.deadline < date.today() and obj.status != 'done'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']