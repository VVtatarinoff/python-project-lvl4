import logging

from task_manager.forms.statuses_forms import CreateStatusForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.views.general import CreateMixin, UpdateMixin

logger = logging.getLogger(__name__)


class Statuses(LoginRequiredMessage, SimpleTableView):
    pass


class CreateStatus(CreateMixin):
    form_class = CreateStatusForm
    pass


class UpdateStatus(UpdateMixin):
    form_class = CreateStatusForm
