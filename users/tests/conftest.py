import itertools

import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse

from task_manager.tests.conftest import (log_user1, setup_users,   # noqa F401
                                         setup_tasks, setup_labels,
                                         setup_statuses,
                                         )
from task_manager.tests.fixtures.db_fixtures import USERS_TEST
import users.views

NOLOGIN_PAGE = {users.views.LIST_VIEW, users.views.CREATE_VIEW, 'login'}

LOGIN_REQUIRED_PAGE_PK = {users.views.DELETE_VIEW,
                          users.views.UPDATE_VIEW,
                          }


@pytest.fixture(params=LOGIN_REQUIRED_PAGE_PK)
def site_path(request, setup_tasks):   # noqa 811
    path = reverse(request.param, kwargs={'pk': 1})
    return path


@pytest.fixture(params=['author', 'executor'])
def bound_user(client, setup_tasks, request):   # noqa 811
    """ for delete user testing two bound cases: author and executor
    It is crucial two have two instances in user model that matches
    criterias
    - instance that is author for some task do not executor
                for any task including this
    - instance that is executor for some task do not executor
                for any task including this
    At those cases tests would not intersect"""

    authors = User.objects.annotate(
        Count('author')).filter(author__count__gt=0).values_list('id')
    authors_set = set(itertools.chain(*authors))
    executors = User.objects.annotate(
        Count('executor')).filter(executor__count__gt=0).values_list('id')
    executors_set = set(itertools.chain(*executors))
    authors_only = authors_set - executors_set
    executors_only = executors_set - authors_set
    if not authors_only or not executors_only:
        raise Exception('wrong tests configuration:'
                        ' no unique author and executor')
    if request.param == 'author':
        user = User.objects.get(id=list(authors_only)[0])
    else:
        user = User.objects.get(id=list(executors_only)[0])

    client.force_login(user)
    return user


@pytest.fixture
def user1_details():
    user1 = USERS_TEST[0].copy()
    user1['password1'] = user1['password']
    user1['password2'] = user1['password']
    return user1
