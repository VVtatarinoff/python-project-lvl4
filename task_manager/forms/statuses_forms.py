from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from task_manager.models import Status, Label, Task


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
        print(self.fields)

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'author', 'labels')
        # exclude = ('author',)


class FilterTaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FilterTaskForm, self).__init__(*args, **kwargs)
        print('In filter form: ', kwargs)
        print(args)
        print(kwargs)
        st_choices = [('', '-------------')] + list(Status.objects.values_list('id', 'name', named=True).all())
        self.fields['status'] = forms.ChoiceField(label=_('Status'), required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}, ),
                                   choices=st_choices,
                                                  initial=kwargs['initial']['status'])
        self.fields['executor'].required = False
        self.fields['labels'].required = False
        self.fields['author'].required = False

    class Meta:
        model = Task
        fields = ('status', 'executor', 'labels', 'author')
