import pytest
from django.db.models import Count
from django.urls import reverse

import statuses.views
import labels.views
from statuses.models import Status
from labels.models import Label

TEST_CONFIGURATIONS = [(Label, labels.views), (Status, statuses.views)]


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_create_get(client, log_user1, configuration):
    model, views = configuration
    response = client.get(reverse(views.CREATE_VIEW))
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(views.CREATE_TITLE) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_create_post(client, log_user1, setup_tasks, configuration):
    model, views = configuration
    initial_count = model.objects.all().count()
    new_name = 'veryvery important'
    response = client.post(reverse(views.CREATE_VIEW),
                           {'name': new_name})
    created_item = model.objects.get(name=new_name)
    assert created_item
    assert response.status_code == 302
    assert response.url == reverse(views.LIST_VIEW)
    assert model.objects.all().count() == initial_count + 1
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(views.MESSAGE_CREATE_SUCCESS)


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_view(client, log_user1, setup_tasks, configuration):
    model, views = configuration
    response = client.get(reverse(views.LIST_VIEW))
    content = response.rendered_content
    lines = content.count('</tr')
    lines_expected = model.objects.all().count()
    assert lines == lines_expected
    assert content.find(views.LIST_TITLE) > 0
    names = model.objects.values_list('name').all()
    inclusions = list(map(lambda x: content.find(*x) > 0, names))
    assert all(inclusions)
    assert content.find(reverse(views.CREATE_VIEW)) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_update_html(client, log_user1, setup_tasks, configuration):
    model, views = configuration
    item = model.objects.all().first()
    response = client.get(reverse(views.UPDATE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(views.UPDATE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_update_post(
        client, log_user1, setup_tasks, configuration):
    model, views = configuration
    item = model.objects.all().first()
    new_name = item.name + 'test'
    response = client.post(reverse(views.UPDATE_VIEW,
                                   kwargs={'pk': item.id}),
                           {'name': new_name})
    assert response.status_code == 302
    assert response.url == reverse(views.LIST_VIEW)
    updated_item = model.objects.get(id=item.id)
    assert updated_item.name == new_name
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(views.MESSAGE_UPDATE_SUCCESS)


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_delete_html(client, log_user1, setup_tasks, configuration):
    model, views = configuration
    item = model.objects.all().first()
    response = client.get(reverse(views.DELETE_VIEW,
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find(views.QUESTION_DELETE) > 0
    assert content.find(views.DELETE_TITLE) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_delete_unbound(client, log_user1,
                        setup_tasks, configuration):
    model, views = configuration
    count_before = model.objects.all().count()
    unbound_item = model.objects.annotate(
        Count('task')).filter(task__count=0).first()
    response = client.post(reverse(views.DELETE_VIEW,
                                   kwargs={'pk': unbound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(views.LIST_VIEW)
    with pytest.raises(Exception) as e:
        model.objects.get(id=unbound_item.id)
    assert e.match('matching query does not exist')
    count_after = model.objects.all().count()
    assert count_after == count_before - 1
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(views.MESSAGE_DELETE_SUCCESS)


@pytest.mark.django_db
@pytest.mark.parametrize('configuration', TEST_CONFIGURATIONS)
def test_delete_bound(client, log_user1, setup_tasks, configuration):
    model, views = configuration
    count_before = model.objects.all().count()
    bound_item = model.objects.annotate(
        Count('task')).filter(task__count__gt=0).first()
    response = client.post(reverse(views.DELETE_VIEW,
                                   kwargs={'pk': bound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(views.LIST_VIEW)
    item_after = model.objects.get(id=bound_item.id)
    assert item_after.name == bound_item.name
    count_after = model.objects.all().count()
    assert count_after == count_before
    # force flashing of message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(views.DELETE_CONSTRAINT_MESSAGE)
