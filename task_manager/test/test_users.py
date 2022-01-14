from django.contrib.auth.models import User
import pytest
import logging
from django.urls import reverse

from task_manager.test.fixtures.db_fixtures import USERS_TEST, NEW_USER
from task_manager.views.constants import (CREATE_LINKS, USER_CATEGORY,
                                          FLASH_NO_PERMISSION_EDIT,
                                          UPDATE_TITLES, UPDATE_LINKS,
                                          DELETE_LINKS, CREATE_TITLES,
                                          LIST_LINKS, TITLES)


logger = logging.getLogger(__name__)

FIRST_USER = USERS_TEST[0]

REGISTER_PATH = reverse(CREATE_LINKS[USER_CATEGORY])
VIEW_PATH = reverse(LIST_LINKS[USER_CATEGORY])
UPDATE_PATH = UPDATE_LINKS[USER_CATEGORY]
DELETE_PATH = DELETE_LINKS[USER_CATEGORY]

LIST_TITLE = TITLES[USER_CATEGORY]
UPDATE_TITLE = UPDATE_TITLES[USER_CATEGORY]
CREATE_TITLE = CREATE_TITLES[USER_CATEGORY]


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ('method="post"', 'name="username"',
                          'name="first_name"', 'name="last_name"',
                          'name="password1"', 'name="password2"',
                          CREATE_TITLE))
def test_register_get(client, test_string):
    response = client.get(REGISTER_PATH)
    content = response.rendered_content
    assert content.find(test_string) > 0


@pytest.mark.django_db
def test_register_post_normal(client):
    response = client.post(REGISTER_PATH, NEW_USER)
    created_user = User.objects.get(username=NEW_USER['username'])
    assert created_user
    assert created_user.get_full_name() == NEW_USER['full_name']
    assert response.status_code == 302
    expected_url = reverse("login")
    assert response.url == expected_url
    assert not response.wsgi_request.user.is_authenticated
    login_status = client.login(
        username=NEW_USER['username'],
        password=NEW_USER['password1'])
    assert login_status


@pytest.mark.django_db
def test_register_post_the_same_name(client, setup_users, user1_details):
    keep_name = user1_details['first_name']
    user1_details['first_name'] = user1_details['first_name'] + 'test'
    response = client.post(REGISTER_PATH, user1_details)
    assert User.objects.all().count() == len(setup_users)
    assert response.status_code == 200
    check_user = User.objects.get(username=user1_details['username'])
    assert check_user.first_name == keep_name


@pytest.mark.django_db
def test_login_logout(client, setup_users, user1_details):
    response = client.get(reverse("login"))
    content = response.rendered_content
    assert content.find('method="post"') > 0
    assert content.find('name="username"') > 0
    assert content.find('name="password"') > 0
    response = client.post(reverse("login"), user1_details)
    assert response.wsgi_request.user.is_authenticated
    response = client.get(reverse("logout"))
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
@pytest.mark.parametrize('user', USERS_TEST)
def test_view_users(client, setup_users, user):
    response = client.get(VIEW_PATH)
    content = response.rendered_content
    lines = content.count('</tr')
    assert lines == len(setup_users)
    assert content.find(LIST_TITLE) > 0
    fullname = user['first_name'] + ' ' + user['last_name']
    assert content.find(fullname) > 0


@pytest.mark.django_db
@pytest.mark.parametrize('test_string',
                         ('method="post"', 'name="username"',
                          'name="first_name"', 'name="last_name"',
                          'name="password1"', 'name="password2"',
                          FIRST_USER['username'], FIRST_USER['first_name'],
                          FIRST_USER['last_name']))
def test_update_html(client, setup_users, test_string, log_user1):
    response = client.get(reverse(UPDATE_PATH, kwargs={'pk': log_user1.id}))
    assert response.status_code == 200
    content = response.rendered_content
    assert content.find(test_string) > 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    'update_field', ['first_name', 'last_name', 'username', 'password'])
def test_update_self(client, setup_users, update_field,
                     log_user1, user1_details):
    updated_user_data = user1_details.copy()
    updated_user_data[update_field] = updated_user_data[update_field] + 'test'
    updated_user_data['password1'] = updated_user_data['password']
    updated_user_data['password2'] = updated_user_data['password']
    response = client.post(reverse(UPDATE_PATH, kwargs={'pk': log_user1.id}),
                           updated_user_data)
    user_db = User.objects.get(id=log_user1.id)
    assert not response.wsgi_request.user.is_authenticated
    assert response.url == VIEW_PATH
    assert user_db.username == updated_user_data['username']
    assert user_db.first_name == updated_user_data['first_name']
    assert user_db.last_name == updated_user_data['last_name']
    credetails = {'username': updated_user_data['username'],
                  'password': updated_user_data['password']}
    login_status = client.login(**credetails)
    assert login_status


@pytest.mark.django_db
def test_update_not_selfuser(client, setup_users, log_user1):
    other_id = 2
    user2_before_request = list(User.objects.filter(id=other_id).values_list())
    response = client.post(reverse(UPDATE_PATH, kwargs={'pk': other_id}),
                           NEW_USER)
    user2_after_request = list(User.objects.filter(id=other_id).values_list())
    assert response.wsgi_request.user.is_authenticated
    assert user2_before_request == user2_after_request
    # force to flash message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(FLASH_NO_PERMISSION_EDIT) > 0


@pytest.mark.django_db
def test_delete_self(client, setup_users, log_user1):
    response = client.post(reverse(DELETE_PATH, kwargs={'pk': log_user1.id}))
    with pytest.raises(Exception) as e:
        User.objects.get(username=log_user1.username)
    assert e.match('User matching query does not exist')
    assert User.objects.all().count() == len(setup_users) - 1
    assert response.status_code == 302
    assert response.url == VIEW_PATH


@pytest.mark.django_db
def test_delete_not_self(client, setup_users, log_user1):
    response = client.post(reverse(DELETE_PATH, kwargs={'pk': 2}))
    assert User.objects.all().count() == len(setup_users)
    assert User.objects.get(id=2)
    assert response.status_code == 302
    assert response.url == VIEW_PATH


@pytest.mark.django_db
def test_delete_bound(client, setup_tasks, bound_user):
    initial_count = User.objects.all().count()
    response = client.post(reverse(DELETE_PATH,
                                   kwargs={'pk': bound_user.id}))
    assert User.objects.all().count() == initial_count
    assert User.objects.get(id=bound_user.id)
    assert response.status_code == 302
    assert response.url == VIEW_PATH
