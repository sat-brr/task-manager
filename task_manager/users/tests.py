from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
import json
import os
# Create your tests here.


HTTP_FOUND = HTTPStatus.FOUND
FIXTURES_PATH = os.path.abspath('task_manager/fixtures')
TEST_DATA_PATH = os.path.join(FIXTURES_PATH, 'test_data.json')


class TestUserCrud(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        file = open(TEST_DATA_PATH).read()
        self.test_data = json.loads(file)

    def test_create_user(self):
        response = self.client.post(reverse("create_user"),
                                    data=self.test_data['new']['user'])

        self.assertEqual(response.status_code, HTTP_FOUND)

        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.last().username,
                         self.test_data['new']['user']['username'])

    def test_update_user(self):
        user = get_user_model().objects.first()

        response = self.client.post(reverse('update_user', args=[user.pk]),
                                    data=self.test_data['new']['user'])

        updated_user = get_user_model().objects.first()

        self.assertEqual(response.status_code, HTTP_FOUND)
        self.assertEqual(updated_user.first_name,
                         self.test_data['new']['user']['first_name'])
        self.assertEqual(updated_user.username,
                         self.test_data['new']['user']['username'])

    def test_delete_user(self):
        user = get_user_model().objects.first()

        response = self.client.post(reverse("delete_user", args=[user.pk]))

        self.assertEqual(response.status_code, HTTP_FOUND)

        self.assertEqual(get_user_model().objects.count(), 0)
