import pytest
from django.urls import reverse

from task_manager.tests.conftest import (log_user1, setup_users,   # noqa F401
                                         setup_tasks, setup_labels,
                                         setup_statuses, )
import tasks.views

LOGIN_REQUIRED_PAGE = {tasks.views.LIST_VIEW,
                       tasks.views.CREATE_VIEW}
LOGIN_REQUIRED_PAGE_PK = {tasks.views.DETAIL_VIEW,
                          tasks.views.DELETE_VIEW,
                          tasks.views.UPDATE_VIEW,
                          }


@pytest.fixture(params=LOGIN_REQUIRED_PAGE | LOGIN_REQUIRED_PAGE_PK)
def site_path(request, setup_tasks):    # noqa 811
    if request.param in LOGIN_REQUIRED_PAGE:
        path = reverse(request.param)
    else:
        path = reverse(request.param, kwargs={'pk': 1})
    return path


@pytest.fixture(params=[
    ({}, {}),
    ({'labels': [1]}, {'labels': 1}),
    ({'status': 1}, {'status': 1}),
    ({'executor': 1}, {'executor': 1}),
    ({'executor': 1, 'author': 'on'}, {'executor': 1}),
    ({'author': 'on'}, {})
])
def filter_data(request, log_user1, setup_tasks):   # noqa 811
    filter, query_data = request.param
    if filter.get('self_tasks'):
        query_data['author'] = log_user1.id
    return filter, query_data
