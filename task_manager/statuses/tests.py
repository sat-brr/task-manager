from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
import os
import json
# Create your tests here.


HTTP_FOUND = HTTPStatus.FOUND
FIXTURES_PATH = os.path.abspath('task_manager/fixtures')
TEST_DATA_PATH = os.path.join(FIXTURES_PATH, 'test_data.json')


class TestStatusCrud(TestCase):
    fixtures = ['status.json', 'user.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        file = open(TEST_DATA_PATH).read()
        self.test_data = json.loads(file)

    def test_create_status(self):

        response = self.client.post(reverse('create_status'),
                                    data=self.test_data['new']['status'])
        self.assertEqual(response.status_code, HTTP_FOUND)

        new_status = Status.objects.last()

        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(new_status.name,
                         self.test_data['new']['status']['name'])

    def test_update_status(self):
        status = Status.objects.first()

        response = self.client.post(reverse('update_status', args=[status.pk]),
                                    data=self.test_data['new']['status'])

        updated_status = Status.objects.first()

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(updated_status.name,
                         self.test_data['new']['status']['name'])

    def test_delete_status(self):
        status = Status.objects.first()

        response = self.client.post(reverse('delete_status', args=[status.pk]))

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(Status.objects.count(), 0)
