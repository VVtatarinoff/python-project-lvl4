import logging

from task_manager.forms.statuses_forms import CreateLabelForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.views.general import CreateMixin, UpdateMixin

logger = logging.getLogger(__name__)


class Labels(LoginRequiredMessage, SimpleTableView):
    pass


class CreateLabel(CreateMixin):
    form_class = CreateLabelForm
    pass


class UpdateLabel(UpdateMixin):
    form_class = CreateLabelForm
