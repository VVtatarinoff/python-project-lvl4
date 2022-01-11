import pytest
import logging
from django.urls import reverse

from task_manager.models import Status
from task_manager.views.constants import CREATE_LINKS, STATUS_CATEGORY
from task_manager.views.constants import UPDATE_TITLES, UPDATE_LINKS
from task_manager.views.constants import DELETE_LINKS, DELETE_TITLES
from task_manager.views.constants import LIST_LINKS, TITLES
from task_manager.views.constants import CREATE_TITLES

logger = logging.getLogger(__name__)

REGISTER_PATH = reverse(CREATE_LINKS[STATUS_CATEGORY])
VIEW_PATH = reverse(LIST_LINKS[STATUS_CATEGORY])
UPDATE_PATH = UPDATE_LINKS[STATUS_CATEGORY]
DELETE_PATH = DELETE_LINKS[STATUS_CATEGORY]

LIST_TITLE = TITLES[STATUS_CATEGORY]
UPDATE_TITLE = UPDATE_TITLES[STATUS_CATEGORY]
CREATE_TITLE = CREATE_TITLES[STATUS_CATEGORY]
DELETE_TITLE = DELETE_TITLES[STATUS_CATEGORY]
" *************'C' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ('method="post"', 'name="name"',
                          CREATE_TITLE))
def test_create_status_get(client, test_string, log_user1):
    response = client.get(REGISTER_PATH)
    content = response.rendered_content
    assert content.find(test_string) > 0


@pytest.mark.django_db
def test_create_status_post(client, log_user1, setup_statuses):
    status_name = 'veryvery important'
    response = client.post(REGISTER_PATH, {'name': status_name})
    created_status = Status.objects.get(name=status_name)
    assert created_status
    assert response.status_code == 302
    assert response.url == VIEW_PATH
    assert Status.objects.all().count() == len(setup_statuses) + 1


" *************'R' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('status_name',
                         ['first status name', "second status name",
                          "third status name"])
def test_view_users(client, log_user1, setup_statuses, status_name):
    response = client.get(VIEW_PATH)
    content = response.rendered_content
    lines = content.count('<tr>')
    assert lines == len(setup_statuses)
    assert content.find(LIST_TITLE) > 0
    assert content.find(status_name) > 0


" *************'U' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ('method="post"', 'name="name"', UPDATE_TITLE))
def test_update_html(client, test_string, log_user1, setup_statuses):
    response = client.get(reverse(UPDATE_PATH,
                                  kwargs={'pk': setup_statuses[0].id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find(test_string) > 0
    assert content.find(setup_statuses[0].name) > 0


@pytest.mark.django_db
def test_update_post(client, log_user1, setup_statuses):
    new_name = setup_statuses[0].name + 'test'
    response = client.post(reverse(UPDATE_PATH,
                                   kwargs={'pk': setup_statuses[0].id}),
                           {'name': new_name})
    assert response.status_code == 302
    assert response.url == VIEW_PATH
    updated_status = Status.objects.get(id=setup_statuses[0].id)
    assert updated_status.name == new_name


" *************'D' from CRUD  ****************************"


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ('method="post"', DELETE_TITLE))
def test_delete_html(client, test_string, log_user1, setup_statuses):
    response = client.get(reverse(DELETE_PATH,
                                  kwargs={'pk': setup_statuses[0].id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find(test_string) > 0
    assert content.find(setup_statuses[0].name) > 0


@pytest.mark.django_db
def test_delete_unbound_status(client, log_user1, unbound_status):
    count_before = Status.objects.all().count()
    response = client.post(reverse(DELETE_PATH,
                                   kwargs={'pk': unbound_status.id}))
    assert response.status_code == 302
    assert response.url == VIEW_PATH
    with pytest.raises(Exception) as e:
        Status.objects.get(id=unbound_status.id)
    assert e.match('Status matching query does not exist')
    count_after = Status.objects.all().count()
    assert count_after == count_before - 1


@pytest.mark.django_db
def test_delete_bound_status(client, log_user1, bound_status):
    count_before = Status.objects.all().count()
    response = client.post(reverse(DELETE_PATH,
                                   kwargs={'pk': bound_status.id}))
    assert response.status_code == 302
    assert response.url == VIEW_PATH
    status_after = Status.objects.get(id=bound_status.id)
    assert status_after.name == bound_status.name
    count_after = Status.objects.all().count()
    assert count_after == count_before
