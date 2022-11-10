from django.test import TestCase, Client
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
# Create your tests here.


class TestTask(TestCase):

    def setUp(self):
        self.client = Client()
        self.status_name = 'NewStatus'
        self.username = 'tester'
        self.password = 'Testing2020'
        self.task_name = 'TESTING'
        User.objects.create_user(username=self.username,
                                 password=self.password)
        Status.objects.create(name=self.status_name)

        self.client.login(username=self.username,
                          password=self.password)

        self.new_status = Status.objects.get(name=self.status_name)
        self.new_user = User.objects.get(username=self.username)

    def test_create_task(self):
        response = self.client.post('/tasks/create/', data={
            'name': self.task_name,
            'status': self.new_status.id
        })

        self.assertEqual(response.status_code, 302)

        tasks = Task.objects.all()
        task = Task.objects.get(name=self.task_name)

        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task.status.id, self.new_status.pk)
        self.assertEqual(task.author.id, self.new_user.pk)

    def test_update_task(self):
        task = Task.objects.create(name=self.task_name,
                                   status=self.new_status,
                                   author=self.new_user)

        response = self.client.post(f"/tasks/{str(task.pk)}/update/",
                                    data={'name': 'TESTING555',
                                          'status': self.new_status.id})

        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(pk=task.id)

        self.assertEqual(task.name, 'TESTING555')

    def test_delete_task(self):
        task = Task.objects.create(name=self.task_name,
                                   status=self.new_status,
                                   author=self.new_user)

        response = self.client.post(f"/tasks/{str(task.pk)}/delete/")

        self.assertEqual(response.status_code, 302)

        tasks = Task.objects.all()

        self.assertEqual(tasks.count(), 0)
