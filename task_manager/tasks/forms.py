from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django import forms


class CreateTaskForm(forms.ModelForm):
    name = forms.CharField(label=_('Имя'),
                           widget=forms.TextInput(attrs={'class': 'form-input'})
                           )
    description = forms.CharField(label=_('Описание'),
                                  required=False,
                                  widget=forms.Textarea(attrs={
                                                        'cols': '40',
                                                        'rows': '10',
                                                        'class': 'form-input'})
                                  )
    status = forms.ModelChoiceField(label=_('Статус'),
                                    queryset=Status.objects.all())
    executor = forms.ModelChoiceField(label=_('Исполнитель'),
                                      queryset=User.objects.all(),
                                      required=False)
    labels = forms.ModelMultipleChoiceField(label=_('Метки'),
                                            queryset=Label.objects.all(),
                                            required=False)

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
