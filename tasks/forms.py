import logging

import django_filters
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms import ModelForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django_filters import filters

from task_manager.models import Label, Task, Status

logger = logging.getLogger(__name__)


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


class TaskFilter(django_filters.FilterSet):
    st_choices = Status.objects.values_list('id', 'name', named=True).all()
    status = filters.ChoiceFilter(label=_('Status'),
                                  choices=st_choices)
    lb_choices = Label.objects.values_list('id', 'name', named=True).all()
    labels = filters.ChoiceFilter(label=_('Label'),
                                  choices=lb_choices)
    ex_choices = User.objects.values_list(
        'id', Concat('first_name', Value(' '), 'last_name'),
        named=True).all()
    executor = filters.ChoiceFilter(label=_('Executor'),
                                    choices=ex_choices)
    self_task = filters.BooleanFilter(label=_('Only my tasks'),
                                      widget=forms.CheckboxInput(),
                                      method='filter_self',
                                      field_name='self_task')

    def filter_self(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
