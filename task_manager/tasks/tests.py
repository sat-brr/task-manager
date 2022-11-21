from django.test import TestCase, Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.urls import reverse
from http import HTTPStatus
import os
import json
# Create your tests here.


FIXTURES_PATH = os.path.abspath('task_manager/fixtures')
TEST_DATA_PATH = os.path.join(FIXTURES_PATH, 'test_data.json')
HTTP_FOUND = HTTPStatus.FOUND


class TestTask(TestCase):
    fixtures = ['task.json', 'user.json', 'status.json', 'label.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.user = user
        self.client.force_login(user)
        self.status = Status.objects.first()
        self.label = Label.objects.first()
        file = open(TEST_DATA_PATH).read()
        self.test_data = json.loads(file)

    def test_create_task(self):

        response = self.client.post(reverse('create_task'),
                                    data=self.test_data['new']['task'])

        self.assertEqual(response.status_code, HTTP_FOUND)

        task = Task.objects.get(name=self.test_data['new']['task']['name'])

        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.status.id,
                         self.test_data['new']['task']['status'])
        self.assertEqual(task.author.id,
                         self.test_data['new']['task']['author'])
        self.assertEqual(task.labels.first().pk,
                         self.test_data['new']['task']['labels'])

    def test_update_task(self):
        task = Task.objects.first()

        response = self.client.post(reverse('update_task', args=[task.id]),
                                    data=self.test_data['new']['task'])

        self.assertEqual(response.status_code, HTTP_FOUND)

        updated_task = Task.objects.get(pk=task.pk)

        self.assertEqual(updated_task.name,
                         self.test_data['new']['task']['name'])
        self.assertEqual(updated_task.executor.pk,
                         self.test_data['new']['task']['executor'])

    def test_delete_task(self):
        task = Task.objects.first()

        response = self.client.post(reverse('delete_task', args=[task.id]))

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(Task.objects.count(), 0)
