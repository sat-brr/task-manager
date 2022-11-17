from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.


class TestStatusCrud(TestCase):
    fixtures = ['status.json', 'user.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)

    def test_create_status(self):
        context = {
            'name': 'NewStatus'
        }

        response = self.client.post(reverse('create_status'),
                                    data=context)
        self.assertEqual(response.status_code, 302)

        new_status = Status.objects.last()

        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(new_status.name, context['name'])

    def test_update_status(self):
        status = Status.objects.first()
        context = {
            'name': 'UpdatedStatus'
        }

        response = self.client.post(reverse('update_status', args=[status.pk]),
                                    data=context)

        updated_status = Status.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_status.name, context['name'])

    def test_delete_status(self):
        status = Status.objects.first()

        response = self.client.post(reverse('delete_status', args=[status.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)
