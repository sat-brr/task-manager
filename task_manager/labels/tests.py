from django.test import TestCase, Client
from django.contrib.auth.models import User
from task_manager.labels.models import Label
# Create your tests here.


class TestLabels(TestCase):

    def setUp(self):
        self.client = Client()
        self.name = 'NewStatus'
        self.username = 'tester'
        self.password = 'Testing2020'
        User.objects.create_user(username=self.username,
                                 password=self.password)
        self.label_name = 'TestMark'
        self.login = self.client.login(username=self.username,
                                       password=self.password)

    def test_create_label(self):
        self.login
        response = self.client.post('/labels/create/', data={
            'name': self.label_name
        })

        self.assertEqual(response.status_code, 302)

        label = Label.objects.get(name=self.label_name)
        labels = Label.objects.all()

        self.assertEqual(labels.count(), 1)
        self.assertEqual(label.name, self.label_name)

    def test_update_label(self):
        self.login
        self.client.post('/labels/create/', data={
            'name': self.label_name
        })

        label = Label.objects.get(name=self.label_name)

        response = self.client.post(f'/labels/{str(label.id)}/update/', data={
            'name': 'NewNameMark'
        })

        self.assertEqual(response.status_code, 302)

        label_updated = Label.objects.get(name='NewNameMark')

        self.assertNotEqual(label.name, label_updated.name)
        self.assertEqual(label.id, label_updated.id)
        self.assertEqual(label_updated.name, 'NewNameMark')

    def test_delete_label(self):
        self.login
        self.client.post('/labels/create/', data={
            'name': self.label_name
        })

        label = Label.objects.get(name=self.label_name)

        response = self.client.post(f'/labels/{str(label.id)}/delete/')

        self.assertEqual(response.status_code, 302)

        labels = Label.objects.all()

        self.assertEqual(labels.count(), 0)
