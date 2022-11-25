from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import load_test_data
from django.contrib.messages import get_messages
# Create your tests here.


class TestUserCrud(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']

    def setUp(self):
        self.client = Client()
        self.user_1 = get_user_model().objects.first()
        self.user_2 = get_user_model().objects.last()
        self.client.force_login(self.user_1)
        self.test_data = load_test_data()
        self.count = get_user_model().objects.count()

    def test_create_user(self):
        self.client.logout()

        response = self.client.post(reverse("create_user"),
                                    data=self.test_data['new']['user'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

        self.assertEqual(get_user_model().objects.count(), self.count + 1)
        self.assertEqual(get_user_model().objects.last().username,
                         self.test_data['new']['user']['username'])

    def test_create_user_without_required_fields(self):

        response = self.client.post(reverse("create_user"),
                                    data=self.test_data['new']['bad_user'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(get_user_model().objects.count(), self.count)
        self.assertFalse(get_user_model().objects.filter(
            username=self.test_data['new']['bad_user']['username']))

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

        message = list(get_messages(response.wsgi_request))

        self.assertEqual(message[0].tags, 'error')
        self.assertRedirects(response, reverse('users_list'))
        self.assertNotEqual(self.user_2.username,
                            self.test_data['new']['user']['username'])

    def test_delete_another_user(self):
        response = self.client.post(reverse("delete_user",
                                            args=[self.user_2.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))

        message = list(get_messages(response.wsgi_request))

        self.assertEquals(message[0].tags, 'error')
        self.assertEqual(get_user_model().objects.count(), self.count)
        self.assertTrue(get_user_model().objects.filter(pk=self.user_2.pk))

    def test_delete_used_user(self):
        response = self.client.post(reverse("delete_user",
                                            args=[self.user_1.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        message = list(get_messages(response.wsgi_request))

        self.assertEqual(message[0].tags, 'error')
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(get_user_model().objects.count(), self.count)
        self.assertTrue(get_user_model().objects.filter(pk=self.user_1.pk))

    def test_delete_unused_user(self):
        self.client.force_login(self.user_2)

        response = self.client.post(reverse("delete_user",
                                            args=[self.user_2.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(get_user_model().objects.count(), self.count - 1)
        self.assertFalse(get_user_model().objects.filter(pk=self.user_2.pk))
