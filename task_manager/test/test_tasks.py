import itertools
import pytest
import logging
from django.urls import reverse

from task_manager.models import Task
from task_manager.test.fixtures.db_fixtures import NEW_TASK
from task_manager.views.constants import (CREATE_LINKS, TASK_CATEGORY,
                                          DELETE_TITLES,
                                          UPDATE_TITLES, UPDATE_LINKS,
                                          DELETE_LINKS,
                                          LIST_LINKS, TITLES,
                                          CREATE_TITLES)

logger = logging.getLogger(__name__)

CREATE_PATH = reverse(CREATE_LINKS[TASK_CATEGORY])
VIEW_PATH = reverse(LIST_LINKS[TASK_CATEGORY])
UPDATE_PATH = UPDATE_LINKS[TASK_CATEGORY]
DELETE_PATH = DELETE_LINKS[TASK_CATEGORY]

LIST_TITLE = TITLES[TASK_CATEGORY]
UPDATE_TITLE = UPDATE_TITLES[TASK_CATEGORY]
CREATE_TITLE = CREATE_TITLES[TASK_CATEGORY]
DELETE_TITLE = DELETE_TITLES[TASK_CATEGORY]


# *************'C' from CRUD  ****************************"


@pytest.mark.django_db
def test_create_get(client, log_user1):
    response = client.get(CREATE_PATH)
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="description"') > 0
    assert content.find('name="name"') > 0
    assert content.find('name="status"') > 0
    assert content.find('name="executor"') > 0
    assert content.find('name="labels"') > 0
    assert content.find(CREATE_TITLE) > 0


@pytest.mark.django_db
def test_create_status_post(client, log_user1, setup_tasks):
    initial_count = Task.objects.all().count()
    response = client.post(CREATE_PATH, NEW_TASK)
    created_item = Task.objects.get(name=NEW_TASK['name'])
    assert response.status_code == 302
    assert response.url == VIEW_PATH
    assert Task.objects.all().count() == initial_count + 1
    assert created_item.description == NEW_TASK['description']
    assert created_item.executor.id == NEW_TASK['executor']
    assert created_item.author.id == log_user1.id
    assert created_item.status.id == NEW_TASK['status']
    assigned_labels = list(itertools.chain(
        *created_item.labels.values_list('id')))
    assert assigned_labels == NEW_TASK['labels']


# *************'R' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ['name', 'author__first_name', 'author__last_name',
                          'executor__first_name', 'executor__last_name',
                          'status__name'])
def test_view_tasks(client, log_user1, setup_tasks, test_string):
    response = client.get(VIEW_PATH)
    content = response.rendered_content
    lines = content.count('<tr>')
    lines_expected = Task.objects.all().count()
    assert lines == lines_expected
    assert content.find(LIST_TITLE) > 0
    names = Task.objects.values_list(test_string).all()
    inclusions = list(map(lambda x: content.find(str(*x)) > 0, names))
    assert all(inclusions)


@pytest.mark.django_db
def test_view_tasks_filter(client, log_user1, setup_tasks):
    pass
