from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DeleteView, CreateView
from django.views import View
from task_manager.mixins import MyLoginRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.labels.models import Label
from task_manager.labels.forms import CreateLabelForm
# Create your views here.


class LabelsPage(MyLoginRequired, View):

    def get(self, request):
        labels = Label.objects.all()
        template_name = 'labels/labels.html'
        return render(request, template_name, context={
            'labels': labels
        })


class CreateLabel(MyLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'
    success_url = '/labels/'
    success_message = _("Метка успешно создана")


class UpdateLabel(MyLoginRequired, SuccessMessageMixin, UpdateView):

    form_class = CreateLabelForm
    model = Label
    template_name = 'labels/update_label.html'
    success_url = '/labels/'
    success_message = _("Метка успешно изменена")


class DeleteLabel(MyLoginRequired, SuccessMessageMixin, DeleteView):

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
