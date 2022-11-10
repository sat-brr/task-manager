from django.test import TestCase
from django.test import Client
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
# Create your tests here.


class TestCreateStatus(TestCase):

    def setUp(self):
        self.client = Client()
        self.name = 'NewStatus'
        self.username = 'tester'
        self.password = 'Testing2020'

        User.objects.create_user(username=self.username,
                                 password=self.password)

    def test_create_status(self):
        self.client.login(username=self.username,
                          password=self.password)
        response = self.client.post('/statuses/create/', data={
            'name': self.name
        })

        statuses = Status.objects.all()
        new_status = Status.objects.get(name=self.name)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(statuses.count(), 1)
        self.assertEqual(new_status.name, self.name)


class TestUpdateStatus(TestCase):

    def setUp(self):
        self.client = Client()
        self.name = 'NewStatus'
        self.username = 'tester'
        self.password = 'Testing2020'

        User.objects.create_user(username=self.username,
                                 password=self.password)

        self.client.login(username=self.username,
                          password=self.password)

        self.client.post('/statuses/create/', data={
            'name': self.name
        })

        new_status = Status.objects.get(name=self.name)
        self.pk_status = new_status.id

    def test_update_status(self):
        response = self.client.post(f"/statuses/{str(self.pk_status)}/update/",
                                    data={'name': 'UpdateStatus'})

        status = Status.objects.get(pk=self.pk_status)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(status.name, 'UpdateStatus')


class TestDeleteStatus(TestCase):

    def setUp(self):
        self.client = Client()
        self.name = 'NewStatus'
        self.username = 'tester'
        self.password = 'Testing2020'

        User.objects.create_user(username=self.username,
                                 password=self.password)

        self.client.login(username=self.username,
                          password=self.password)

        self.client.post('/statuses/create/', data={
            'name': self.name
        })

        new_status = Status.objects.get(name=self.name)
        self.pk_status = new_status.id

    def test_delete_status(self):
        response = self.client.post(f'/statuses/{str(self.pk_status)}/delete/')

        statuses = Status.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(statuses.count(), 0)
