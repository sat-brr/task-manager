from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from task_manager.mixins import MyLoginRequired
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.tasks.forms import CreateTaskForm, TasksFilterForm
from django.contrib import messages
from django_filters.views import FilterView
# Create your views here.


class TasksPage(MyLoginRequired, FilterView):
    filterset_class = TasksFilterForm
    template_name = 'tasks/tasks.html'
    model = Task


class CreateTask(MyLoginRequired, SuccessMessageMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_url = '/tasks/'
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(MyLoginRequired, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/update_task.html'
    model = Task
    form_class = CreateTaskForm
    success_url = '/tasks/'
    success_message = _("Задача успешно изменена")


class DeleteTask(MyLoginRequired, DeleteView, SuccessMessageMixin):

    template_name = 'tasks/delete_task.html'
    model = Task
    success_url = '/tasks/'
    success_message = _("Задача успешно удалена")

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        if task.author.id != request.user.id:
            messages.error(request, _("Задачу может удалить только её автор"))
            return redirect('/tasks/')
        return render(request, self.template_name, context={
            'task': task
        })


class DetailTask(MyLoginRequired, DetailView):
    model = Task
    template_name = 'tasks/detail_task.html'
