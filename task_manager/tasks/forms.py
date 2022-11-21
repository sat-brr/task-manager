from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.functions import Concat
from django.db.models import Value
import django_filters
from django import forms


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class CreateTaskForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'),
                           widget=forms.TextInput(attrs={'class': 'form-input'})
                           )
    description = forms.CharField(label=_('Description'),
                                  required=False,
                                  widget=forms.Textarea(attrs={
                                                        'cols': '40',
                                                        'rows': '10',
                                                        'class': 'form-input'})
                                  )
    status = forms.ModelChoiceField(label=_('Status'),
                                    queryset=Status.objects.all())
    executor = MyModelChoiceField(label=_('Executor'),
                                  queryset=User.objects.all(),
                                  required=False)
    labels = forms.ModelMultipleChoiceField(label=_('Labels'),
                                            queryset=Label.objects.all(),
                                            required=False)

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]


class TasksFilterForm(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(label=_('Status'),
                                              queryset=Status.objects.all())
    all_executives = User.objects.values_list(
        'id',
        Concat('first_name', Value(' '), 'last_name'),
        named=True,
    ).all()

    executor = django_filters.ChoiceFilter(label=_('Executor'),
                                           choices=all_executives)
    labels = django_filters.ModelChoiceFilter(label=_('Label'),
                                              queryset=Label.objects.all())
    author = django_filters.BooleanFilter(widget=forms.CheckboxInput,
                                          field_name='author',
                                          method='only_author',
                                          label=_("Only your own tasks"))

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "author"]

    def only_author(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(author=user.pk)
        return queryset
