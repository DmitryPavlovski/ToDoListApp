from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
import json


class MainViewTestCase(TestCase):
    """Test class for view main"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="john.smith", password="secret")
        self.auth_client = Client()
        self.auth_client.login(username="john.smith", password="secret")
        self.not_auth_client = Client()
        self.task_data = {'title': 'Test task',
                          'description': '', 'userId': self.user.id}

    def test_for_unauthenticated_user(self):
        """Send GET request on main view without authenticated"""
        response = self.not_auth_client.get(reverse('main'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/user/login/')

    def test_for_authenticated_user(self):
        """Send GET request on main view with authenticated"""
        response = self.auth_client.get(reverse('main'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/index/')


class IndexViewTestCase(TestCase):
    """Test class for view index"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="john.smith", password="secret")
        self.auth_client = Client()
        self.auth_client.login(username="john.smith", password="secret")
        self.not_auth_client = Client()
        self.task_data = {'title': 'Test task',
                          'description': '', 'userId': self.user.id}

    def test_get_request_with_authenticated_user(self):
        """Send GET request on index view with authenticated"""
        response = self.auth_client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/index/')

    def test_post_request_and_form_with_authenticated_user(self):
        """Send POST request on index view with form data with authenticated"""
        old_count = len(Task.objects.all())
        response = self.auth_client.post(
            reverse('index'), data=self.task_data, follow=True)
        new_count = len(Task.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/index/')
        self.assertEqual(old_count+1, new_count)

    def test_get_request_with_unauthenticated_user(self):
        """Send GET request on index view without authenticated"""
        response = self.not_auth_client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user/login/')

    def test_post_request_and_form_with_unauthenticated_user(self):
        """Send POST request on index view with form data without authenticated"""
        old_count = len(Task.objects.all())
        response = self.not_auth_client.post(
            reverse('index'), data=self.task_data, follow=True)
        new_count = len(Task.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user/login/')
        self.assertEqual(old_count, new_count)


class ToDoOperationTestCase(TestCase):
    """Test class for operation with task"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="john.smith", password="secret")
        self.auth_client = Client()
        self.auth_client.login(username="john.smith", password="secret")
        self.not_auth_client = Client()
        self.task_data = {'title': 'Test task',
                          'description': '1234', 'userId': self.user.id}

    def test_create_task_item_with_authenticated_user(self):
        """Send request on create new task with authenticated"""
        old_count = len(Task.objects.all())
        response = self.auth_client.post(
            reverse('new'), data=self.task_data, follow=True)
        new_count = len(Task.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/index/')
        self.assertEqual(old_count+1, new_count)

    def test_delete_task_item_with_authenticated_user(self):
        """Send request on delete task with authenticated"""
        old_count = len(Task.objects.all())
        task = Task.objects.create(
            title=self.task_data['title'], userId=self.user, description=self.task_data['description'])
        response = self.auth_client.get(
            reverse('delete_task', kwargs={'pk': task.id}), follow=True)
        new_count = len(Task.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/index/')
        self.assertEqual(new_count, old_count)

    def test_completed_task_Item_with_authenticated_user(self):
        """Send request on completed task with authenticated"""
        task = Task.objects.create(
            title=self.task_data['title'], userId=self.user, description=self.task_data['description'])
        old_task_completed = task.completed
        response = self.auth_client.get(
            reverse('complate_task', kwargs={'pk': task.id}), follow=True)
        task.refresh_from_db()
        new_task_completed = task.completed
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/index/')
        self.assertEqual(old_task_completed, not new_task_completed)

    def test_create_task_item_with_unauthenticated_user(self):
        """Send request on create new task without authenticated"""
        response = self.not_auth_client.post(
            reverse('new'), data=self.task_data, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_update_task_item_with_unauthenticated_user(self):
        """Send request on update task without authenticated"""
        task = Task.objects.create(
            title=self.task_data['title'], userId=self.user, description=self.task_data['description'])
        response = self.not_auth_client.post(
            reverse('update_task', kwargs={'pk': task.id}), data=self.task_data, follow=True)
        self.assertEqual(response.status_code, 404)


    def test_delete_task_item_with_unauthenticated_user(self):
        """Send request on delete task without authenticated"""
        response = self.not_auth_client.get(
            reverse('delete_task', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_completed_task_Item_with_unauthenticated_user(self):
        """Send request on completed task without authenticated"""
        response = self.not_auth_client.get(
            reverse('complate_task', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 404)
