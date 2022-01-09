import logging

from django import forms
from django.db.models import Value
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
        self.fields['name'] = forms.CharField(label=_('Name'),
                                              max_length=150,
                                              widget=forms.TextInput(attrs={
                                                  'class': 'form-control',
                                                  'placeholder': _('Name')}))
        self.fields['description'] = \
            forms.CharField(label=_('Description'), max_length=150,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'placeholder': _('Description'),
                                'cols': 40,
                                'rows': 10}))
        self.fields['status'].label = _('Status')
        self.fields['status'].widget.attrs['class'] = 'form-control'
        ex_choices = [('', '-------------')] + list(
            User.objects.values_list('id', Concat('first_name',
                                                  Value(' '), 'last_name'),
                                     named=True).all())
        self.fields['executor'].choices = ex_choices
        self.fields['executor'].label = _('Executor')
        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['class'] = 'form-control'
        self.fields['labels'].label = _('Labels')
        self.fields['labels'].widget.attrs['class'] = 'form-control'
        self.fields['labels'].required = False

    def save(self, commit=True):
        self.instance.author_id = self.aor_id
        return super().save(commit)

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')


class FilterTaskForm(ModelForm):
    EMPTY = [('', '-------------')]

    def __init__(self, *args, **kwargs):
        super(FilterTaskForm, self).__init__(*args, **kwargs)
        form_class = {'class': 'form-control'}
        st_choices = self.EMPTY + list(
            Status.objects.values_list('id', 'name', named=True).all())
        self.fields['status'] = \
            forms.ChoiceField(label=_('Status'), required=False,
                              widget=forms.Select(attrs=form_class),
                              choices=st_choices,
                              initial=kwargs['initial']['status'])
        ex_choices = self.EMPTY + list(User.objects.values_list(
            'id', Concat('first_name', Value(' '), 'last_name'),
            named=True).all())
        self.fields['executor'] = \
            forms.ChoiceField(label=_('Executor'), required=False,
                              widget=forms.Select(
                                  attrs=form_class),
                              choices=ex_choices,
                              initial=kwargs['initial']
                              ['executor'])
        lbl_choices = self.EMPTY + list(
            Label.objects.values_list('id',
                                      'name',
                                      named=True).all())
        self.fields['labels'] = forms.ChoiceField(label=_('Label'),
                                                  required=False,
                                                  widget=forms.Select(
                                                      attrs=form_class, ),
                                                  choices=lbl_choices,
                                                  initial=kwargs['initial']
                                                  ['labels'])
        self.fields['self_tasks'] = \
            forms.BooleanField(label=_('Only my tasks'),
                               required=False,
                               widget=forms.CheckboxInput(
                                   attrs={
                                       'class': 'form-check-input',
                                       'name': 'self_tasks'}
                               ),
                               initial=False)

    class Meta:
        model = Task
        fields = ('status', 'executor', 'labels')
