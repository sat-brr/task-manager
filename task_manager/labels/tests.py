from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from django.urls import reverse
# Create your tests here.


class TestLabelsCrud(TestCase):
    fixtures = ['user.json', 'label.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)

    def test_create_label(self):
        context = {
            'name': 'NewLabel'
        }
        response = self.client.post(reverse('create_label'),
                                    data=context)

        self.assertEqual(response.status_code, 302)

        label = Label.objects.last()

        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(label.name, context['name'])

    def test_update_label(self):
        label = Label.objects.first()
        context = {
            'name': 'UpdatedLabel'
        }

        response = self.client.post(reverse('update_label', args=[label.pk]),
                                    data=context)

        self.assertEqual(response.status_code, 302)

        label_updated = Label.objects.first()

        self.assertEqual(label_updated.name, context['name'])

    def test_delete_label(self):
        label = Label.objects.first()

        response = self.client.post(reverse('delete_label', args=[label.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 0)
