from django.shortcuts import redirect
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from task_manager.mixins import CustomLoginRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from task_manager.tasks.forms import CreateTaskForm, TasksFilterForm
from django.contrib import messages
from django_filters.views import FilterView
from django.urls import reverse_lazy
# Create your views here.


class TasksPage(CustomLoginRequired, FilterView):

    filterset_class = TasksFilterForm
    template_name = 'tasks/tasks.html'
    model = Task


class CreateTask(CustomLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(CustomLoginRequired, SuccessMessageMixin, UpdateView):

    template_name = 'tasks/update_task.html'
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно изменена")


class DeleteTask(CustomLoginRequired, UserPassesTestMixin,
                 SuccessMessageMixin, DeleteView):

    template_name = 'tasks/delete_task.html'
    model = Task
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно удалена")

    def test_func(self):
        self.object = self.get_object()
        return self.object.author.id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, _("Задачу может удалить только её автор"))
        return redirect(reverse_lazy('tasks_list'))


class DetailTask(CustomLoginRequired, DetailView):

    model = Task
    template_name = 'tasks/detail_task.html'
