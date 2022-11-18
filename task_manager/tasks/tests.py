from django.test import TestCase, Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.urls import reverse
# Create your tests here.


class TestTask(TestCase):
    fixtures = ['task.json', 'user.json', 'status.json', 'label.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.user = user
        self.client.force_login(user)
        self.status = Status.objects.first()
        self.label = Label.objects.first()

    def test_create_task(self):
        context = {
            'name': 'NewTask',
            'author': self.user.id,
            'status': self.status.id,
            'executor': self.user.id,
            'labels': self.label.id
        }

        response = self.client.post(reverse('create_task'),
                                    data=context)

        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name=context['name'])

        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.status.id, context['status'])
        self.assertEqual(task.author.id, context['author'])
        self.assertEqual(task.labels.all().first().pk, context['labels'])

    def test_update_task(self):
        task = Task.objects.first()
        context = {
            'name': 'UpdatedTask',
            'executor': self.user.id,
            'status': self.status.id
        }

        response = self.client.post(reverse('update_task', args=[task.id]),
                                    data=context)

        self.assertEqual(response.status_code, 302)

        updated_task = Task.objects.get(pk=task.pk)

        self.assertEqual(updated_task.name, context['name'])
        self.assertEqual(updated_task.executor.pk, context['executor'])

    def test_delete_task(self):
        task = Task.objects.first()

        response = self.client.post(reverse('delete_task', args=[task.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
