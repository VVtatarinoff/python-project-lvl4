import pytest
from django.contrib.auth.models import User

from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from task_manager.tests.fixtures.db_fixtures import LABELS_TEST
from task_manager.tests.fixtures.db_fixtures import TASKS_TEST
from task_manager.tests.fixtures.db_fixtures import USERS_TEST
from task_manager.tests.fixtures.db_fixtures import STATUSES_TEST


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


@pytest.fixture
def log_user1(client, setup_users):
    credetail = {'username': USERS_TEST[0]['username'],
                 'password': USERS_TEST[0]['password']}
    user = User.objects.get(username=credetail['username'])
    client.login(**credetail)
    return user
