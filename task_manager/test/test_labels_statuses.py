import pytest
from django.db.models import Count
from django.urls import reverse

from task_manager.views.constants import (CREATE_LINKS, MODELS, LIST_LINKS,
                                          TITLES, UPDATE_LINKS, DELETE_LINKS,
                                          DELETE_TITLES, LABEL_CATEGORY,
                                          STATUS_CATEGORY, CREATE_TITLES,
                                          TASK_CATEGORY, QUESTION_DELETE,
                                          DELETE_CONSTRAINT_MESSAGE)

# ************** tests for labels and statuses ***************
# *************'C' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('category', [LABEL_CATEGORY, STATUS_CATEGORY])
def test_create_get(client, log_user1, category):
    response = client.get(reverse(CREATE_LINKS[category]))
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(CREATE_TITLES[category]) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('category', [LABEL_CATEGORY, STATUS_CATEGORY])
def test_create_status_post(client, log_user1, setup_tasks, category):
    model = MODELS[category]
    initial_count = model.objects.all().count()
    new_name = 'veryvery important'
    response = client.post(reverse(CREATE_LINKS[category]),
                           {'name': new_name})
    created_item = model.objects.get(name=new_name)
    assert created_item
    assert response.status_code == 302
    assert response.url == reverse(LIST_LINKS[category])
    assert model.objects.all().count() == initial_count + 1


# *************'R' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('category', [LABEL_CATEGORY, STATUS_CATEGORY])
def test_view_labels_statuses(client, log_user1, setup_tasks, category):
    model = MODELS[category]
    response = client.get(reverse(LIST_LINKS[category]))
    content = response.rendered_content
    lines = content.count('<tr>')
    lines_expected = model.objects.all().count()
    assert lines == lines_expected
    assert content.find(TITLES[category]) > 0
    names = model.objects.values_list('name').all()
    inclusions = list(map(lambda x: content.find(*x) > 0, names))
    assert all(inclusions)


# *************'U' from CRUD  ****************************
#               also tasks update html tested in next function

@pytest.mark.django_db
@pytest.mark.parametrize('category', [LABEL_CATEGORY, STATUS_CATEGORY,
                                      TASK_CATEGORY])
def test_update_html_labels_statuses(client, log_user1, setup_tasks, category):
    model = MODELS[category]
    item = model.objects.all().first()
    response = client.get(reverse(UPDATE_LINKS[category],
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="name"') > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('category', [LABEL_CATEGORY, STATUS_CATEGORY])
def test_update_post_labels_statuses(
        client, log_user1, setup_tasks, category):
    model = MODELS[category]
    item = model.objects.all().first()
    new_name = item.name + 'test'
    response = client.post(reverse(UPDATE_LINKS[category],
                                   kwargs={'pk': item.id}),
                           {'name': new_name})
    assert response.status_code == 302
    assert response.url == reverse(LIST_LINKS[category])
    updated_item = model.objects.get(id=item.id)
    assert updated_item.name == new_name


# *************'D' from CRUD  ****************************"
#               also tasks delete html tested in next function

@pytest.mark.django_db
@pytest.mark.parametrize('category', [
    LABEL_CATEGORY, STATUS_CATEGORY, TASK_CATEGORY])
def test_delete_html_labels_statuses(
        client, log_user1, setup_tasks, category):
    model = MODELS[category]
    item = model.objects.all().first()
    response = client.get(reverse(DELETE_LINKS[category],
                                  kwargs={'pk': item.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find(QUESTION_DELETE) > 0
    assert content.find(DELETE_TITLES[category]) > 0
    assert content.find(item.name) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('category', [STATUS_CATEGORY, LABEL_CATEGORY])
def test_delete_unbound_labels_statuses(
        client, log_user1, setup_tasks, category):
    model = MODELS[category]
    count_before = model.objects.all().count()
    unbound_item = model.objects.annotate(
        Count('task')).filter(task__count=0).first()
    response = client.post(reverse(DELETE_LINKS[category],
                                   kwargs={'pk': unbound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_LINKS[category])
    with pytest.raises(Exception) as e:
        model.objects.get(id=unbound_item.id)
    assert e.match('matching query does not exist')
    count_after = model.objects.all().count()
    assert count_after == count_before - 1


@pytest.mark.django_db
@pytest.mark.parametrize('category', [STATUS_CATEGORY, LABEL_CATEGORY])
def test_delete_bound_labels_statuses(
        client, log_user1, setup_tasks, category):
    model = MODELS[category]
    count_before = model.objects.all().count()
    bound_item = model.objects.annotate(
        Count('task')).filter(task__count__gt=0).first()
    response = client.post(reverse(DELETE_LINKS[category],
                                   kwargs={'pk': bound_item.id}))
    assert response.status_code == 302
    assert response.url == reverse(LIST_LINKS[category])
    item_after = model.objects.get(id=bound_item.id)
    assert item_after.name == bound_item.name
    count_after = model.objects.all().count()
    assert count_after == count_before
    # force to flash message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(DELETE_CONSTRAINT_MESSAGE[category])
