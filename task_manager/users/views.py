from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from task_manager.users.forms import RegisterForm, LoginForm
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# Create your views here.


class UserCreate(FormView):

    def get(self, request):
        form_class = RegisterForm()
        template_name = 'users/user_create.html'
        return render(request, template_name, context={
            'form': form_class
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            messages.success(request, _('Пользователь успешно зарегистрирован'))
            return redirect('/login/')
        return render(request, 'users/user_create.html', context={
            'form': form
        })


class UserLogin(View):
    form_class = LoginForm()

    def get(self, request):
        template_name = 'users/user_login.html'
        return render(request, template_name, context={
            'form': self.form_class
        })

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, _('Вы залогинены'))
            return redirect('/')
        else:
            messages.error(request, _("""Пожалуйста, введите правильные
                                    имя пользователя и пароль.
                                    Оба поля могут быть чувствительны
                                    к регистру."""))
            return render(request, 'users/user_login.html', context={
                'form': self.form_class
            })


class UserLogout(View):
    def post(self, request):
        logout(request)
        messages.info(request, _('Вы разлогинены'))
        return redirect('/')


class UsersPage(View):
    def get(self, request):
        users = User.objects.all()
        if not request.user.is_authenticated:
            return render(request, 'users/users.html', context={
                'users': users
            })
        else:
            return render(request, 'users/users_auth.html', context={
                'users': users
            })


class UpdateUser(SuccessMessageMixin, UpdateView):
    template_name = 'users/update_user.html'
    model = User
    form_class = RegisterForm
    success_url = '/users/'
    success_message = _("Пользователь успешно изменён.")

    def get(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("""Вы не авторизованы!
                                      Пожалуйста, выполните вход."""))
            return redirect('/login/')
        if request.user.id != pk:
            messages.error(request, _("""У вас нет прав для
                                    изменения другого пользователя."""))
            return redirect('/users/')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class RemoverUser(SuccessMessageMixin, DeleteView):
    template_name = 'users/remove_user.html'
    model = User
    success_url = '/users/'
    success_message = _("Пользователь успешно удалён.")

    def get(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, _('Вы не авторизованы! Выполните вход.'))
            return redirect('/login/')
        if request.user.id != pk:
            messages.error(request, _("""У Вас нет прав для
                                    удаления другого пользователя."""))
            return redirect('/users/')
        return render(request, self.template_name, context={
            'user': request.user
        })

    def post(self, request, *args, **kwargs):
        if self.get_object().author.all() or self.get_object().tasks.all():
            messages.error(request, _("""Невозможно удалить пользователя,
                                      потому что он используется"""))
            return redirect('/users/')
        return super().post(request, *args, **kwargs)
