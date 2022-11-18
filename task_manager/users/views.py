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
    success_message = _('Пользователь успешно зарегистрирован')


class UserLogin(SuccessMessageMixin, LoginView):

    form_class = LoginForm
    template_name = 'users/user_login.html'
    next_page = reverse_lazy("main")
    success_message = _('Вы залогинены')


class UserLogout(LogoutView):
    next_page = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('Вы разлогинены'))
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
    success_message = _("Пользователь успешно изменён.")

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.pk == self.object.pk

    def handle_no_permission(self):
        messages.error(self.request, _("""У вас нет прав для
                                    изменения другого пользователя."""))
        return redirect(reverse_lazy('users_list'))


class RemoverUser(CustomLoginRequired, UserPassesTestMixin,
                  SuccessMessageMixin, DeleteView):

    template_name = 'users/delete_user.html'
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно удалён.")

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.pk == self.object.pk

    def handle_no_permission(self):
        messages.error(self.request, _("""У Вас нет прав для
                                  удаления другого пользователя."""))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        if self.get_object().author.first() or self.get_object().tasks.first():
            messages.error(request, _("""Невозможно удалить пользователя,
                                      потому что он используется"""))
            return redirect(reverse_lazy('users_list'))
        return super().post(request, *args, **kwargs)
