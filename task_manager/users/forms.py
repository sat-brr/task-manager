from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True,
                                 label=_("First name"))
    last_name = forms.CharField(max_length=30, required=True,
                                label=_("Last name"))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",
                  "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
