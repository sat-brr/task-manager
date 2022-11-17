from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from task_manager.users.forms import RegisterForm, LoginForm
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


class UserLogin(View):

    form_class = LoginForm()
    template_name = 'users/user_login.html'

    def get(self, request):
        return render(request, self.template_name, context={
            'form': self.form_class
        })

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, _('Вы залогинены'))
            return redirect(reverse_lazy('home'))
        else:
            messages.error(request, _("""Пожалуйста, введите правильные
                                    имя пользователя и пароль.
                                    Оба поля могут быть чувствительны
                                    к регистру."""))
            return render(request, self.template_name, context={
                'form': self.form_class
            })


class UserLogout(View):

    def post(self, request):
        logout(request)
        messages.info(request, _('Вы разлогинены'))
        return redirect(reverse_lazy('home'))


class UsersPage(ListView):

    model = User
    template_name = ''
    context_object_name = 'users'

    def get(self, request):
        if not request.user.is_authenticated:
            self.template_name = "users/users.html"
        else:
            self.template_name = "users/users_auth.html"
        return super().get(request)


class UpdateUser(CustomLoginRequired, SuccessMessageMixin, UpdateView):

    template_name = 'users/update_user.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно изменён.")

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, _("""У вас нет прав для
                                    изменения другого пользователя."""))
            return redirect(reverse_lazy('users_list'))
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class RemoverUser(CustomLoginRequired, SuccessMessageMixin, DeleteView):

    template_name = 'users/delete_user.html'
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно удалён.")

    def get(self, request, pk):
        if request.user.id != pk:
            messages.error(request, _("""У Вас нет прав для
                                    удаления другого пользователя."""))
            return redirect(reverse_lazy('users_list'))
        return super().get(request)

    def post(self, request, *args, **kwargs):
        if self.get_object().author.first() or self.get_object().tasks.first():
            messages.error(request, _("""Невозможно удалить пользователя,
                                      потому что он используется"""))
            return redirect(reverse_lazy('users_list'))
        return super().post(request, *args, **kwargs)
