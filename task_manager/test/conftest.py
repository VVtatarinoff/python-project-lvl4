import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.models import Label, Task, Status
from task_manager.test.fixtures.db_fixtures import LABELS_TEST
from task_manager.test.fixtures.db_fixtures import TASKS_TEST
from task_manager.test.fixtures.db_fixtures import USERS_TEST
from task_manager.test.fixtures.db_fixtures import STATUSES_TEST
from task_manager.views.constants import *  # noqa 403

NOLOGIN_PAGE = {'home', LIST_LINKS[USER_CATEGORY],          # noqa 405
                'login', CREATE_LINKS[USER_CATEGORY], }     # noqa 405
LOGIN_REQUIRED_PAGE = {LIST_LINKS[STATUS_CATEGORY],         # noqa 405
                       LIST_LINKS[LABEL_CATEGORY],          # noqa 405
                       LIST_LINKS[TASK_CATEGORY],           # noqa 405
                       CREATE_LINKS[STATUS_CATEGORY],       # noqa 405
                       CREATE_LINKS[LABEL_CATEGORY],        # noqa 405
                       CREATE_LINKS[TASK_CATEGORY], }       # noqa 405
LOGIN_REQUIRED_PAGE_PK = {'tasks_detail',
                          DELETE_LINKS[STATUS_CATEGORY],    # noqa 405
                          DELETE_LINKS[LABEL_CATEGORY],     # noqa 405
                          DELETE_LINKS[TASK_CATEGORY],      # noqa 405
                          DELETE_LINKS[USER_CATEGORY],      # noqa 405
                          UPDATE_LINKS[STATUS_CATEGORY],    # noqa 405
                          UPDATE_LINKS[LABEL_CATEGORY],     # noqa 405
                          UPDATE_LINKS[TASK_CATEGORY],      # noqa 405
                          UPDATE_LINKS[USER_CATEGORY],      # noqa 405
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
def log_user1(client):
    credetail = {'username': USERS_TEST[0]['username'],
            'password': USERS_TEST[0]['password']}
    user = User.objects.get(username=credetail['username'])
    client.login(**credetail)
    return user


@pytest.fixture
def user1_details():
    user1 = USERS_TEST[0].copy()
    user1['password1'] = user1['password']
    user1['password2'] = user1['password']
    return user1
