from task_manager.statuses.models import Status
from django import forms


class CreateStatusForm(forms.ModelForm):
    name = forms.CharField(label=('Имя'),
                           widget=forms.TextInput(attrs={'class': 'form-input'})
                           )

    class Meta:
        model = Status
        fields = ("name",)
