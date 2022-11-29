from django import forms
from django.forms import DateField

from mailSender1 import settings
from .models import Clients


class ClientCreateForm(forms.ModelForm):
    birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Clients
        fields = ['name', 'surname', 'birth', 'email']
        labels = {'birth': 'DD.MM.YYYY'}
        help_texts = {'birth': 'DD.MM.YYYY'}



