import logging

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class UserMixin(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Name')}),
        max_length=150,
        label=_('Name'))
    last_name = forms.CharField(label=_('Last name'),
                                max_length=150,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Last name')}))
    username = forms.CharField(label=_('User name'),
                               max_length=150,
                               help_text=_('Required field. Not more than 150 '
                                           'symbols, only letters, numbers '
                                           'and symbols @/./+/-/_.'),
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': _('User name')}))
    password1 = forms.CharField(label=_('Password'),
                                help_text=_('Your password should '
                                            'be at least 3 symbols'),
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Password')}))
    password2 = forms.CharField(label=_('Confirmation of password'),
                                help_text=_('Please repeat your '
                                            'password for confirmation'),
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Confirmation of password')}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2')


class RegisterUserForm(UserMixin, UserCreationForm):
    pass


class ChangeUserForm(UserMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _('The two password fields didn’t match.'),
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('User name'),
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': _('User name')}))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': _('Password')}))
