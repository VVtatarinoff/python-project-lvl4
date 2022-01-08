import logging

from django import forms
from django.db.models import Value, F, Func
from django.db.models.functions import Concat
from django.forms import ModelForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from task_manager.models import Status, Label, Task

logger = logging.getLogger(__name__)


class CreateStatusForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Name')}),
        max_length=100,
        label=_('Name'))

    class Meta:
        model = Status
        fields = ('name',)


class CreateLabelForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Name')}),
        max_length=100,
        label=_('Name'))

    class Meta:
        model = Label
        fields = ('name',)


class CreateTaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.aor_id = kwargs.pop('id', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        logger.info(self.fields)

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'author', 'labels')
        # exclude = ('author',)


class FilterTaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FilterTaskForm, self).__init__(*args, **kwargs)
        st_choices = [('', '-------------')] + list(Status.objects.values_list('id', 'name', named=True).all())
        self.fields['status'] = forms.ChoiceField(label=_('Status'), required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}, ),
                                   choices=st_choices,
                                                  initial=kwargs['initial']['status'])
        ex_choices = [('', '-------------')] + list(User.objects.values_list('id', Concat('first_name',
                                                                                          Value(' '), 'last_name'),
                                                                             named=True).all())
        self.fields['executor'] = forms.ChoiceField(label=_('Executor'), required=False,
                                                  widget=forms.Select(attrs={'class': 'form-control'}, ),
                                                  choices=ex_choices,
                                                  initial=kwargs['initial']['executor'])
        lbl_choices = [('', '-------------')] + list(Label.objects.values_list('id', 'name', named=True).all())
        self.fields['labels'] = forms.ChoiceField(label=_('Label'), required=False,
                                                    widget=forms.Select(attrs={'class': 'form-control'}, ),
                                                    choices=lbl_choices,
                                                    initial=kwargs['initial']['labels'])
        self.fields['self_tasks'] = forms.BooleanField(label=_('Only my tasks'), required=False,
                                                   widget=forms.CheckboxInput(attrs={'class':
                                                                                         'form-check-input',
                                                                                     'name':'self_tasks'}, ),
                                                   initial=False)


    class Meta:
        model = Task
        fields = ('status', 'executor', 'labels')
