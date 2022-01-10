import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.models import Label, Task, Status
from task_manager.test.fixtures.db_fixtures import LABELS_TEST
from task_manager.test.fixtures.db_fixtures import TASKS_TEST
from task_manager.test.fixtures.db_fixtures import USERS_TEST
from task_manager.test.fixtures.db_fixtures import STATUSES_TEST

NOLOGIN_PAGE = ['home', 'users', 'login', 'registration', ]
LOGIN_REQUIRED_PAGE = ['statuses', 'labels', 'tasks', 'create_status',
                       'create_label', 'create_task',]
LOGIN_REQUIRED_PAGE_PK = ['tasks_detail', 'delete_status', 'delete_label',
                          'delete_task', 'delete_user', 'update_status',
                          'update_label', 'update_task', 'update_user',
                          ]


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
def setup_users(db):
    users = []
    for user in USERS_TEST:
        users.append(User.objects.create(**user))
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


@pytest.fixture(params=LOGIN_REQUIRED_PAGE + LOGIN_REQUIRED_PAGE_PK)
def site_path(request, setup_tasks):
    if request.param in LOGIN_REQUIRED_PAGE:
        path = reverse(request.param)
    else:
        path = reverse(request.param, kwargs={'pk': 1})
    return path


@pytest.fixture
def log_credential():
    return {'username': USERS_TEST[0]['username'],
            'password': USERS_TEST[0]['password']}