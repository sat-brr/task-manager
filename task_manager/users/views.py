from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User
from task_manager.users.forms import RegisterForm, LoginForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.mixins import CustomLoginRequired
from django.urls import reverse_lazy
# Create your views here.


class UserCreate(SuccessMessageMixin, CreateView):

    form_class = RegisterForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')


class UserLogin(SuccessMessageMixin, LoginView):

    form_class = LoginForm
    template_name = 'users/user_login.html'
    next_page = reverse_lazy("home")
    success_message = _('You are logged in')


class UserLogout(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class UsersPage(ListView):

    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UpdateUser(CustomLoginRequired, UserPassesTestMixin,
                 SuccessMessageMixin, UpdateView):

    template_name = 'users/update_user.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully changed")

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _("""You don't have the rights to
                                       other user's changes"""))
        return redirect(reverse_lazy('users_list'))


class RemoverUser(CustomLoginRequired, UserPassesTestMixin,
                  SuccessMessageMixin, DeleteView):

    template_name = 'users/delete_user.html'
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully deleted.")

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _("""You don't have the rights to
                                       deleting another user."""))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        if self.get_object().author.first() or self.get_object().tasks.first():
            messages.error(request, _("""The user cannot be deleted,
                                      because it is used"""))
            return redirect(reverse_lazy('users_list'))
        return super().post(request, *args, **kwargs)
