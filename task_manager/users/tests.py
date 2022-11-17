from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.


class TestUserCrud(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.first()
        self.client.force_login(user)

    def test_create_user(self):
        context = {
            'first_name': 'Test55',
            'last_name': 'Test66',
            'username': 'Test56',
            'password1': 'Qazrfv4545',
            'password2': 'Qazrfv4545'
        }

        response = self.client.post(reverse("create_user"), data=context)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), 2)

    def test_update_user(self):
        user = get_user_model().objects.first()
        context = {
            'first_name': 'newName',
            'last_name': 'newLast',
            'username': 'NewUser',
            'password1': 'NewPass3535',
            'password2': 'NewPass3535'
        }

        response = self.client.post(reverse('update_user', args=[user.pk]),
                                    data=context)

        updated_user = get_user_model().objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.first_name, context['first_name'])
        self.assertEqual(updated_user.last_name, context['last_name'])

    def test_delete_user(self):
        user = get_user_model().objects.first()

        response = self.client.post(reverse("delete_user", args=[user.pk]))

        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), 0)
