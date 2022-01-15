import pytest
from django.db.models import Count
from django.urls import reverse

from statuses.views import CREATE_VIEW, LIST_VIEW, UPDATE_VIEW, DELETE_VIEW
from statuses.views import LIST_TITLE, CREATE_TITLE, DELETE_TITLE, UPDATE_TITLE
from statuses.views import (MESSAGE_UPDATE_SUCCESS, MESSAGE_DELETE_SUCCESS,
                            MESSAGE_CREATE_SUCCESS, DELETE_CONSTRAINT_MESSAGE,
                            QUESTION_DELETE)
from task_manager.models import Status


@pytest.mark.django_db
def test_create_status_get(client, log_user1):
    response = client.get(reverse(CREATE_VIEW))
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(CREATE_TITLE) > 0


@pytest.mark.django_db
def test_create_status_post(client, log_user1, setup_tasks):
    initial_count = Status.objects.all().count()
    new_name = 'veryvery important'
    response = client.post(reverse(CREATE_VIEW),
                           {'name': new_name})
    created_item = Status.objects.get(name=new_name)
    assert created_item
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    assert Status.objects.all().count() == initial_count + 1
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(MESSAGE_CREATE_SUCCESS)


@pytest.mark.django_db
def test_view_statuses(client, log_user1, setup_tasks):
    response = client.get(reverse(LIST_VIEW))
    content = response.rendered_content
    lines = content.count('</tr')
    lines_expected = Status.objects.all().count()
    assert lines == lines_expected
    assert content.find(LIST_TITLE) > 0
    names = Status.objects.values_list('name').all()
    inclusions = list(map(lambda x: content.find(*x) > 0, names))
    assert all(inclusions)


@pytest.mark.django_db
def test_update_html_statuses(client, log_user1, setup_tasks):
    item = Status.objects.all().first()
    response = client.get(reverse(UPDATE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(UPDATE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
def test_update_post_statuses(
        client, log_user1, setup_tasks):
    item = Status.objects.all().first()
    new_name = item.name + 'test'
    response = client.post(reverse(UPDATE_VIEW,
                                   kwargs={'pk': item.id}),
                           {'name': new_name})
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    updated_item = Status.objects.get(id=item.id)
    assert updated_item.name == new_name
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(MESSAGE_UPDATE_SUCCESS)


@pytest.mark.django_db
def test_delete_html_statuses(client, log_user1, setup_tasks):
    item = Status.objects.all().first()
    response = client.get(reverse(DELETE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find(QUESTION_DELETE) > 0
    assert content.find(DELETE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
def test_delete_unbound_statuses(client, log_user1, setup_tasks):
    count_before = Status.objects.all().count()
    unbound_item = Status.objects.annotate(
        Count('task')).filter(task__count=0).first()
    response = client.post(reverse(DELETE_VIEW,
                                   kwargs={'pk': unbound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    with pytest.raises(Exception) as e:
        Status.objects.get(id=unbound_item.id)
    assert e.match('matching query does not exist')
    count_after = Status.objects.all().count()
    assert count_after == count_before - 1
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(MESSAGE_DELETE_SUCCESS)


@pytest.mark.django_db
def test_delete_bound_statuses(client, log_user1, setup_tasks):
    count_before = Status.objects.all().count()
    bound_item = Status.objects.annotate(
        Count('task')).filter(task__count__gt=0).first()
    response = client.post(reverse(DELETE_VIEW,
                                   kwargs={'pk': bound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
    item_after = Status.objects.get(id=bound_item.id)
    assert item_after.name == bound_item.name
    count_after = Status.objects.all().count()
    assert count_after == count_before
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(DELETE_CONSTRAINT_MESSAGE)
