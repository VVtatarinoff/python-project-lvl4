import logging

from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from task_manager.models import Status

logger = logging.getLogger(__name__)


class StatusForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Name')}),
        max_length=100,
        label=_('Name'))

    class Meta:
        model = Status
        fields = ('name',)
