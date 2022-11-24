from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import TEST_DATA_PATH
import json
# Create your tests here.


class TestUserCrud(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        self.user_1 = get_user_model().objects.first()
        self.user_2 = get_user_model().objects.last()
        self.client.force_login(self.user_1)
        with open(TEST_DATA_PATH, 'r') as file:
            self.test_data = json.loads(file.read())

    def test_create_user(self):
        self.client.logout()

        response = self.client.post(reverse("create_user"),
                                    data=self.test_data['new']['user'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertEqual(get_user_model().objects.last().username,
                         self.test_data['new']['user']['username'])

    def test_update_self_user(self):

        response = self.client.post(reverse('update_user',
                                            args=[self.user_1.pk]),
                                    data=self.test_data['new']['user'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))

        updated_user = get_user_model().objects.get(pk=self.user_1.pk)

        self.assertEqual(updated_user.first_name,
                         self.test_data['new']['user']['first_name'])
        self.assertEqual(updated_user.username,
                         self.test_data['new']['user']['username'])

    def test_update_another_user(self):
        response = self.client.post(reverse('update_user',
                                            args=[self.user_2.pk]),
                                    data=self.test_data['new']['user'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))
        self.assertNotEqual(self.user_2.username,
                            self.test_data['new']['user']['username'])

    def test_delete_another_user(self):
        response = self.client.post(reverse("delete_user",
                                            args=[self.user_2.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertNotEqual(get_user_model().objects.get(pk=self.user_2.pk),
                            None)

    def test_delete_self_user(self):
        response = self.client.post(reverse("delete_user",
                                            args=[self.user_1.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(get_user_model().objects.count(), 1)
