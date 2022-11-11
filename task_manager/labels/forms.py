from django.utils.translation import gettext as _
from django import forms
from task_manager.labels.models import Label


class CreateLabelForm(forms.ModelForm):
    name = forms.CharField(label=_('Имя'),
                           widget=forms.TextInput(attrs={'class': 'form-input'})
                           )

    class Meta:
        model = Label
        fields = ("name",)
