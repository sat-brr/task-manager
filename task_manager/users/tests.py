from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
# Create your tests here.


class TestCreateUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.username = 'test22'
        self.first_name = 'Artur'
        self.last_name = 'Pirojcov'
        self.password = 'Qazrfv4545'

    def test_create_user(self):
        response = self.client.post("/users/create/", data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        users = get_user_model().objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(users.count(), 2)


class TestUpdateUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.username = 'test22'
        self.first_name = 'Artur'
        self.last_name = 'Pirojcov'
        self.password = 'Qazrfv4545'

        self.client.post("/users/create/", data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })

        self.client.post("/login/", data={
            'username': self.username,
            'password': self.password
        })

        self.users = get_user_model().objects.all()
        user = self.users.get(username=self.username)
        self.pk = user.pk

    def test_update_user(self):

        response = self.client.post(f"/users/{str(self.pk)}/update/", data={
            'first_name': 'newName',
            'last_name': 'newLast',
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })

        upd_user = self.users.get(pk=self.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(upd_user.first_name, 'newName')
        self.assertEqual(upd_user.last_name, 'newLast')


class TestDeleteUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.username = 'test22'
        self.first_name = 'Artur'
        self.last_name = 'Pirojcov'
        self.password = 'Qazrfv4545'

        self.client.post("/users/create/", data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })

        self.client.post("/login/", data={
            'username': self.username,
            'password': self.password
        })

        self.users = get_user_model().objects.all()
        user = self.users.get(username=self.username)
        self.pk = user.pk

    def test_delete_user(self):
        response = self.client.post(f"/users/{str(self.pk)}/delete/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 1)
