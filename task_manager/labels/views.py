from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from task_manager.mixins import CustomLoginRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.labels.models import Label
from task_manager.labels.forms import CreateLabelForm
# Create your views here.


class LabelsPage(CustomLoginRequired, ListView):

    model = Label
    template_name = 'labels/labels.html'
    context_object_name='labels'


class CreateLabel(CustomLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'
    success_url = '/labels/'
    success_message = _("Метка успешно создана")


class UpdateLabel(CustomLoginRequired, SuccessMessageMixin, UpdateView):

    form_class = CreateLabelForm
    model = Label
    template_name = 'labels/update_label.html'
    success_url = '/labels/'
    success_message = _("Метка успешно изменена")


class DeleteLabel(CustomLoginRequired, SuccessMessageMixin, DeleteView):

    model = Label
    template_name = 'labels/delete_label.html'
    success_url = '/labels/'
    success_message = _("Метка успешно удалена")

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _("""Невозможно удалить метку,
                                      потому что она используется"""))
            return redirect('/labels/')
        return super().post(request, *args, **kwargs)
