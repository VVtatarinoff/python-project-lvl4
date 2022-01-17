import itertools
import pytest
import logging

from django.urls import reverse
from django.db.models import Q

from tasks.models import Task
from task_manager.tests.fixtures.db_fixtures import NEW_TASK
from tasks.views import (CREATE_VIEW, LIST_VIEW, UPDATE_VIEW,
                         DELETE_VIEW, DETAIL_VIEW)
from tasks.views import (LIST_TITLE, CREATE_TITLE, DELETE_TITLE,
                         UPDATE_TITLE, DETAIL_TITLE)
from tasks.views import (MESSAGE_UPDATE_SUCCESS, MESSAGE_DELETE_SUCCESS,
                         MESSAGE_CREATE_SUCCESS, DELETE_CONSTRAINT_MESSAGE,
                         QUESTION_DELETE)

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_get(client, log_user1):
    response = client.get(reverse(CREATE_VIEW))
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="description"') > 0
    assert content.find('name="name"') > 0
    assert content.find('name="status"') > 0
    assert content.find('name="executor"') > 0
    assert content.find('name="labels"') > 0
    assert content.find(CREATE_TITLE) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', [
    (reverse(CREATE_VIEW), 1, MESSAGE_CREATE_SUCCESS),
    (reverse(UPDATE_VIEW, kwargs={'pk': 1}), 0, MESSAGE_UPDATE_SUCCESS)])
def test_create_update_task_post(client, log_user1,
                                 setup_tasks, configuration):
    """ in this tests two views are tested : update and create"""
    path, incremental, msg = configuration
    initial_count = Task.objects.all().count()
    response = client.post(path, NEW_TASK)
    created_item = Task.objects.get(name=NEW_TASK['name'])
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    assert Task.objects.all().count() == initial_count + incremental
    assert created_item.description == NEW_TASK['description']
    assert created_item.executor.id == NEW_TASK['executor']
    assert created_item.author.id == log_user1.id
    assert created_item.status.id == NEW_TASK['status']
    assigned_labels = list(itertools.chain(
        *created_item.labels.values_list('id')))
    assert assigned_labels == NEW_TASK['labels']
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(msg)


@pytest.mark.django_db
def test_update_html_tasks(client, log_user1, setup_tasks):
    item = Task.objects.all().first()
    response = client.get(reverse(UPDATE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(UPDATE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ['name', 'author__first_name', 'author__last_name',
                          'executor__first_name', 'executor__last_name',
                          'status__name'])
def test_view_tasks(client, log_user1, setup_tasks, test_string, filter_data):
    get_request_args, q = filter_data
    response = client.get(reverse(LIST_VIEW), get_request_args)
    content = response.rendered_content
    lines = content.count('</tr')
    lines_expected = Task.objects.all().filter(Q(**q)).count()
    assert lines == lines_expected
    assert content.find(LIST_TITLE) > 0
    names = Task.objects.filter(Q(**q)).values_list(test_string).all()
    inclusions = list(map(lambda x: content.find(str(*x)) > 0, names))
    assert all(inclusions)
    assert content.find(reverse(CREATE_VIEW)) > 0


@pytest.mark.django_db
def test_delete_html_task(
        client, log_user1, setup_tasks):
    item = Task.objects.all().first()
    response = client.get(reverse(DELETE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find(QUESTION_DELETE) > 0
    assert content.find(DELETE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
def test_delete_own_task(client, log_user1, setup_tasks):
    count_before = Task.objects.all().count()
    item = Task.objects.all().first()
    response = client.post(reverse(DELETE_VIEW,
                                   kwargs={'pk': item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    with pytest.raises(Exception) as e:
        Task.objects.get(id=item.id)
    assert e.match('matching query does not exist')
    count_after = Task.objects.all().count()
    assert count_after == count_before - 1
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(MESSAGE_DELETE_SUCCESS)


@pytest.mark.django_db
def test_delete_not_own_task(client, log_user1, setup_tasks):
    count_before = Task.objects.all().count()
    item = Task.objects.exclude(author=log_user1.id).first()
    response = client.post(reverse(DELETE_VIEW,
                                   kwargs={'pk': item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    assert Task.objects.get(id=item.id)
    count_after = Task.objects.all().count()
    assert count_after == count_before
    # force to flash message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(DELETE_CONSTRAINT_MESSAGE) > 0


@pytest.mark.django_db
def test_detail_view_task(client, log_user1, setup_tasks):
    item = Task.objects.get(id=1)
    response = client.get(reverse(DETAIL_VIEW,
                                  kwargs={'pk': 1}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find(DETAIL_TITLE) > 0
    assert content.find(item.name) > 0
    assert content.find(item.description) > 0
    assert content.find(item.author.get_full_name()) > 0
    assert content.find(item.executor.get_full_name()) > 0
    assert content.find(item.status.name) > 0
    labels = list(itertools.chain(
        *item.labels.values_list('name')))
    inclusions = list(map(lambda x: content.find(str(x)) > 0, labels))
    assert all(inclusions)
    assert content.find(reverse(DELETE_VIEW, kwargs={'pk': 1})) > 0
    assert content.find(reverse(UPDATE_VIEW, kwargs={'pk': 1})) > 0
