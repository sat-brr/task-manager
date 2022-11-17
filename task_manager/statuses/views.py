from django.shortcuts import redirect
from django.utils.translation import gettext as _
from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import CustomLoginRequired
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class CreateStatus(CustomLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно создан")


class StatusesPage(CustomLoginRequired, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class UpdateStatus(CustomLoginRequired, SuccessMessageMixin, UpdateView):

    template_name = 'statuses/update_status.html'
    model = Status
    form_class = CreateStatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно изменён")


class DeleteStatus(CustomLoginRequired, SuccessMessageMixin, DeleteView):

    template_name = 'statuses/delete_status.html'
    model = Status
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно удалён")

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.first():
            messages.error(request, _("""Невозможно удалить статус,
                                      потому что он используется"""))
            return redirect(reverse_lazy('statuses_list'))
        return super().post(request, *args, **kwargs)
