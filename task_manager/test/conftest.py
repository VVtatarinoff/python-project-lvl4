import itertools

import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse

from task_manager.models import Label, Task, Status
from task_manager.test.fixtures.db_fixtures import LABELS_TEST
from task_manager.test.fixtures.db_fixtures import TASKS_TEST
from task_manager.test.fixtures.db_fixtures import USERS_TEST
from task_manager.test.fixtures.db_fixtures import STATUSES_TEST
import statuses.views
import labels.views
import users.views
import tasks.views

NOLOGIN_PAGE = {'home', users.views.LIST_VIEW,
                'login', users.views.CREATE_VIEW, }
LOGIN_REQUIRED_PAGE = {statuses.views.LIST_VIEW,
                       labels.views.LIST_VIEW,
                       tasks.views.LIST_VIEW,
                       statuses.views.CREATE_VIEW,
                       labels.views.CREATE_VIEW,
                       tasks.views.CREATE_VIEW}
LOGIN_REQUIRED_PAGE_PK = {tasks.views.DETAIL_VIEW,
                          statuses.views.DELETE_VIEW,
                          labels.views.DELETE_VIEW,
                          tasks.views.DELETE_VIEW,
                          users.views.DELETE_VIEW,
                          statuses.views.UPDATE_VIEW,
                          labels.views.UPDATE_VIEW,
                          tasks.views.UPDATE_VIEW,
                          users.views.UPDATE_VIEW,
                          }


@pytest.fixture
def setup_labels(db):
    labels = []
    for label in LABELS_TEST:
        labels.append(Label.objects.create(**label))
    return labels


@pytest.fixture
def setup_statuses(db):
    statuses = []
    for status in STATUSES_TEST:
        statuses.append(Status.objects.create(**status))
    return statuses


@pytest.fixture
def setup_users(db, django_user_model):
    users = []
    for user in USERS_TEST:
        users.append(django_user_model.objects.create_user(**user))
    return users


@pytest.fixture
def setup_tasks(db, setup_users, setup_labels, setup_statuses):
    tasks = []
    for task in TASKS_TEST:
        instance = Task.objects.create(name=task['name'],
                                       description=task["description"],
                                       status=setup_statuses[
                                           task['status'] - 1],
                                       author=setup_users[
                                           task['author'] - 1],
                                       executor=setup_users[
                                           task['executor'] - 1])
        for label in task.get('labels', []):
            instance.labels.add(setup_labels[label - 1])
        tasks.append(instance)
    return tasks


@pytest.fixture(params=LOGIN_REQUIRED_PAGE | LOGIN_REQUIRED_PAGE_PK)
def site_path(request, setup_tasks):
    if request.param in LOGIN_REQUIRED_PAGE:
        path = reverse(request.param)
    else:
        path = reverse(request.param, kwargs={'pk': 1})
    return path


@pytest.fixture
def log_user1(client, setup_users):
    credetail = {'username': USERS_TEST[0]['username'],
                 'password': USERS_TEST[0]['password']}
    user = User.objects.get(username=credetail['username'])
    client.login(**credetail)
    return user


@pytest.fixture(params=['author', 'executor'])
def bound_user(client, setup_tasks, request):
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
        raise Exception('wrong test configuration:'
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


@pytest.fixture(params=[
    ({}, {}),
    ({'labels': [1]}, {'labels': 1}),
    ({'status': 1}, {'status': 1}),
    ({'executor': 1}, {'executor': 1}),
    ({'executor': 1, 'author': 'on'}, {'executor': 1}),
    ({'author': 'on'}, {})
])
def filter_data(request, log_user1, setup_tasks):
    filter, query_data = request.param
    if filter.get('self_tasks'):
        query_data['author'] = log_user1.id
    return filter, query_data
