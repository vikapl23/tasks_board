from datetime import date

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Board, Comment, Task


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    board_name = serializers.CharField(source='board.name', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'board', 'board_name', 'status',
                  'start_date', 'deadline', 'is_overdue', 'owner']

    def get_is_overdue(self, obj):
        return obj.deadline < date.today() and obj.status != 'done'

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('Назва задачі має містити щонайменше 3 символи')
        return value

    def validate(self, data):
        # при PATCH частини полів може не бути - беремо їх з наявного запису
        start_date = data.get('start_date', getattr(self.instance, 'start_date', None))
        deadline = data.get('deadline', getattr(self.instance, 'deadline', None))
        if start_date and deadline and deadline < start_date:
            raise serializers.ValidationError('Дедлайн не може бути раніше дати початку')
        return data


class CommentSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'task_title', 'text', 'created_at', 'owner']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Коментар не може бути порожнім')
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token