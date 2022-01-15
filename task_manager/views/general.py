import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

FLASH_LOGINREQUIRED = _('You are not authorized. Please log in')


class LoginRequiredMessage(AccessMixin):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, FLASH_LOGINREQUIRED)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
