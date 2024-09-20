from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task

class TaskAPITests(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        if not User.objects.filter(username=self.username).exists():
            self.user = User.objects.create_user(username=self.username, password=self.password)
        else:
            self.user = User.objects.get(username=self.username)

        self.token = self.get_jwt_token()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            status="new",
            priority="low"
        )

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)

        return str(refresh.access_token)

    def test_create_task(self):
        url = '/api/tasks/'
        data = {
            "title": "New Task",
            "description": "New description",
            "status": "new",
            "priority": "medium"
        }
        initial_task_count = Task.objects.count()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), initial_task_count + 1)

    def test_retrieve_task(self):
        url = f'/api/tasks/{self.task.id}/'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Task")

    def test_update_task(self):
        url = f'/api/tasks/{self.task.id}/'
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "status": "in_progress",
            "priority": "high"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self):
        url = f'/api/tasks/{self.task.id}/'
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
