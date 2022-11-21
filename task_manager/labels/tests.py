from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse
from http import HTTPStatus
import os
import json
# Create your tests here.


HTTP_FOUND = HTTPStatus.FOUND
HTTP_OK = HTTPStatus.OK
FIXTURES_PATH = os.path.abspath('task_manager/fixtures')
TEST_DATA_PATH = os.path.join(FIXTURES_PATH, 'test_data.json')


class TestLabelsCrud(TestCase):
    fixtures = ['user.json', 'label.json', 'task.json', 'status.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)
        file = open(TEST_DATA_PATH).read()
        self.test_data = json.loads(file)

    def test_create_label(self):
        response = self.client.post(reverse('create_label'),
                                    data=self.test_data['new']['label'])

        self.assertEqual(response.status_code, HTTP_FOUND)

        label = Label.objects.last()

        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(label.name,
                         self.test_data['new']['label']['name'])

        response_unique = self.client.post(reverse('create_label'),
                                           data=self.test_data['new']['label'])

        self.assertEqual(response_unique.status_code, HTTP_OK)
        self.assertEqual(Label.objects.count(), 2)

    def test_update_label(self):
        label = Label.objects.first()

        response = self.client.post(reverse('update_label', args=[label.pk]),
                                    data=self.test_data['new']['label'])

        self.assertEqual(response.status_code, HTTP_FOUND)

        label_updated = Label.objects.first()

        self.assertEqual(label_updated.name,
                         self.test_data['new']['label']['name'])

    def test_delete_label(self):
        label = Label.objects.first()

        response = self.client.post(reverse('delete_label', args=[label.pk]))

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(Label.objects.count(), 0)

        new_label = Label.objects.create(name=label.name)
        task = Task.objects.create(author=self.user,
                                   name=self.test_data['new']['task']['name'],
                                   status=Status.objects.first())
        task.labels.set([new_label.id])

        response = self.client.post(reverse('delete_label',
                                            args=[new_label.pk]))

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.first().name, new_label.name)
        self.assertEqual(new_label.task_set.first().id, task.id)
