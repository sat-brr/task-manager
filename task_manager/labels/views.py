from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from task_manager.mixins import CustomLoginRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.labels.models import Label
from task_manager.labels.forms import CreateLabelForm
from django.urls import reverse_lazy
# Create your views here.


class LabelsPage(CustomLoginRequired, ListView):

    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class CreateLabel(CustomLoginRequired, SuccessMessageMixin, CreateView):

    form_class = CreateLabelForm
    template_name = 'labels/create_or_update_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("The label was created successfully")


class UpdateLabel(CustomLoginRequired, SuccessMessageMixin, UpdateView):

    form_class = CreateLabelForm
    model = Label
    template_name = 'labels/create_or_update_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Label changed successfully")


class DeleteLabel(CustomLoginRequired, SuccessMessageMixin, DeleteView):

    model = Label
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("The label was successfully deleted")

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.first():
            messages.error(request, _("""Unable to delete a label,
                                      because it is used"""))
            return redirect(reverse_lazy('labels_list'))
        return super().post(request, *args, **kwargs)
