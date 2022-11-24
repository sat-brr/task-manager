from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import TEST_DATA_PATH
import json
# Create your tests here.


class TestStatusCrud(TestCase):
    fixtures = ['status.json', 'user.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        with open(TEST_DATA_PATH, 'r') as file:
            self.test_data = json.loads(file.read())

    def test_create_status(self):

        response = self.client.post(reverse('create_status'),
                                    data=self.test_data['new']['status'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))

        new_status = Status.objects.last()

        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(new_status.name,
                         self.test_data['new']['status']['name'])

    def test_update_status(self):
        status = Status.objects.first()

        response = self.client.post(reverse('update_status', args=[status.pk]),
                                    data=self.test_data['new']['status'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))

        updated_status = Status.objects.first()

        self.assertEqual(updated_status.name,
                         self.test_data['new']['status']['name'])

    def test_delete_status(self):
        status = Status.objects.first()

        response = self.client.post(reverse('delete_status', args=[status.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), 0)
