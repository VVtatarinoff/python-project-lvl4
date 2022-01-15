import pytest

from django.urls import reverse

from task_manager.views.constants import (MODELS,
                                          UPDATE_LINKS, DELETE_LINKS,
                                          DELETE_TITLES,
                                          TASK_CATEGORY, QUESTION_DELETE,
                                          )


@pytest.mark.django_db
@pytest.mark.parametrize('category', [TASK_CATEGORY])
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
@pytest.mark.parametrize('category', [TASK_CATEGORY])
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
