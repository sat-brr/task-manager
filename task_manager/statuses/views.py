from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from task_manager.mixins import MyLoginRequired
from django.contrib import messages
# Create your views here.


class CreateStatus(MyLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_url = '/statuses/'
    success_message = _("Статус успешно создан")


class StatusesPage(MyLoginRequired, View):

    def get(self, request):
        statuses = Status.objects.all()
        template_name = 'statuses/statuses.html'
        return render(request, template_name, context={
            'statuses': statuses
        })


class UpdateStatus(MyLoginRequired, SuccessMessageMixin, UpdateView):

    template_name = 'statuses/update_status.html'
    model = Status
    form_class = CreateStatusForm
    success_url = '/statuses/'
    success_message = _("Статус успешно изменён")

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().get(request, *args, **kwargs)


class DeleteStatus(MyLoginRequired, SuccessMessageMixin, DeleteView):

    template_name = 'statuses/delete_status.html'
    model = Status
    success_url = '/statuses/'
    success_message = _("Статус успешно удалён")

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _("""Невозможно удалить статус,
                                      потому что он используется"""))
            return redirect('/statuses/')
        return super().post(request, *args, **kwargs)
