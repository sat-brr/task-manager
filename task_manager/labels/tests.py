from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse
# Create your tests here.


class TestLabelsCrud(TestCase):
    fixtures = ['user.json', 'label.json', 'task.json', 'status.json']

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

        new_label = Label.objects.create(name='NewLabel')
        task = Task.objects.create(author=get_user_model().objects.first(),
                                   name='TestDelete',
                                   status=Status.objects.first())
        task.labels.set([new_label.id])

        response = self.client.post(reverse('delete_label',
                                            args=[new_label.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.first().name, new_label.name)
        self.assertEqual(new_label.task_set.first().id, task.id)
