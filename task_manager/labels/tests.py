from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import TEST_DATA_PATH
import json
# Create your tests here.


class TestLabelsCrud(TestCase):
    fixtures = ['user.json', 'label.json', 'task.json', 'status.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.first()
        self.label = Label.objects.first()
        self.client.force_login(self.user)
        with open(TEST_DATA_PATH, 'r') as file:
            self.test_data = json.loads(file.read())

    def test_create_label(self):
        response = self.client.post(reverse('create_label'),
                                    data=self.test_data['new']['label'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_list'))

        label = Label.objects.last()

        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(label.name,
                         self.test_data['new']['label']['name'])

        response_unique = self.client.post(reverse('create_label'),
                                           data=self.test_data['new']['label'])

        self.assertEqual(response_unique.status_code, HTTPStatus.OK)
        self.assertEqual(Label.objects.count(), 2)

    def test_update_label(self):
        response = self.client.post(reverse('update_label',
                                            args=[self.label.pk]),
                                    data=self.test_data['new']['label'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_list'))

        label_updated = Label.objects.first()

        self.assertEqual(label_updated.name,
                         self.test_data['new']['label']['name'])

    def test_delete_label(self):
        response = self.client.post(reverse('delete_label',
                                            args=[self.label.pk]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_used_label(self):
        task = Task.objects.first()
        task.labels.set([self.label.id])

        response = self.client.post(reverse('delete_label',
                                            args=[self.label.id]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.first().id, self.label.id)
