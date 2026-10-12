from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Board, Task


class TaskPermissionsTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.board = Board.objects.create(name='Test Board')
        self.task = Task.objects.create(title='Test task', board=self.board,
                                        start_date=date.today(),
                                        deadline=date.today() + timedelta(days=5),
                                        owner=self.owner)
        self.url = f'/api/tasks/{self.task.pk}/'

    def test_anyone_can_read(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_edit(self):
        response = self.client.patch(self.url, {'status': 'done'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_cannot_edit(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(self.url, {'status': 'done'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_edit(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {'status': 'done'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_short_title_is_rejected(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {'title': 'ab'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_deadline_before_start_is_rejected(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/api/tasks/', {
            'title': 'Wrong dates',
            'board': self.board.pk,
            'start_date': '2026-10-10',
            'deadline': '2026-10-01',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)