import pytest
from django.urls import reverse

import labels.views
from task_manager.tests.conftest import (log_user1, setup_users,   # noqa F401
                                         setup_tasks, setup_labels,
                                         setup_statuses, )

LOGIN_REQUIRED_PAGE = {labels.views.LIST_VIEW,
                       labels.views.CREATE_VIEW,
                       }
LOGIN_REQUIRED_PAGE_PK = {labels.views.DELETE_VIEW,
                          labels.views.UPDATE_VIEW,
                          }


@pytest.fixture(params=LOGIN_REQUIRED_PAGE | LOGIN_REQUIRED_PAGE_PK)
def site_path(request, setup_tasks):    # noqa 811
    if request.param in LOGIN_REQUIRED_PAGE:
        path = reverse(request.param)
    else:
        path = reverse(request.param, kwargs={'pk': 1})
    return path
