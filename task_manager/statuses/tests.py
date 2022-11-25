from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import load_test_data
from django.contrib.messages import get_messages
# Create your tests here.


class TestStatusCrud(TestCase):
    fixtures = ['status.json', 'user.json', 'task.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        self.test_data = load_test_data()
        self.count = Status.objects.count()
        self.used_status = Status.objects.first()
        self.unused_status = Status.objects.last()

    def test_create_status(self):

        response = self.client.post(reverse('create_status'),
                                    data=self.test_data['new']['status'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))

        new_status = Status.objects.last()

        self.assertEqual(Status.objects.count(), self.count + 1)
        self.assertEqual(new_status.name,
                         self.test_data['new']['status']['name'])

    def test_create_status_not_unique(self):

        response = self.client.post(reverse('create_status'), data={
            'name': self.used_status.name
        })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Status.objects.count(), self.count)

    def test_update_status(self):

        response = self.client.post(reverse('update_status',
                                            args=[self.used_status.pk]),
                                    data=self.test_data['new']['status'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))

        updated_status = Status.objects.get(pk=self.used_status.pk)

        self.assertEqual(updated_status.name,
                         self.test_data['new']['status']['name'])

    def test_delete_used_status(self):

        response = self.client.post(reverse('delete_status',
                                            args=[self.used_status.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))

        message = list(get_messages(response.wsgi_request))

        self.assertEqual(message[0].tags, 'error')
        self.assertEqual(Status.objects.count(), self.count)
        self.assertTrue(Status.objects.filter(pk=self.used_status.pk))

    def test_delete_unused_status(self):

        response = self.client.post(reverse('delete_status',
                                            args=[self.unused_status.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), self.count - 1)
        self.assertFalse(Status.objects.filter(pk=self.unused_status.pk))
