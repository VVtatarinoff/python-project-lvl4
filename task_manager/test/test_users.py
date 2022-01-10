from django.contrib.auth.models import User
import pytest
import logging
from django.urls import reverse

from task_manager.test.fixtures.db_fixtures import TEST_DATA
from task_manager.views.constants import CREATE_LINKS, USER_CATEGORY, CREATE_TITLES

logger = logging.getLogger(__name__)
"""
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)"""
REGISTER_PATH = CREATE_LINKS[USER_CATEGORY]
NEW_USER = TEST_DATA['users']['new']
EXISTED_USER = TEST_DATA['users']['existing']

@pytest.mark.django_db
def test_register_get(client):
    response = client.get(reverse(REGISTER_PATH), HTTP_ACCEPT='text/html')
    content = response.rendered_content
    assert content.find(CREATE_TITLES[USER_CATEGORY])
    assert content.find('method="post"')
    assert content.find('name="username"')
    assert content.find('name="first_name"')
    assert content.find('name="second_name"')
    assert content.find('name="password1"')
    assert content.find('name="password2"')


@pytest.mark.django_db
def test_register_post_normal(client):
    response = client.post(reverse(REGISTER_PATH), NEW_USER)
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
def test_register_post_the_same_name(client, setup_users):
    response = client.post(reverse(REGISTER_PATH), EXISTED_USER)
    n = User.objects.all().count()
    assert n == len(setup_users)
    assert response.status_code == 200

