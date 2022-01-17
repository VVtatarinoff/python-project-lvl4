from django.urls import reverse
import pytest

from task_manager.mixins import LOGIN_REQUIRED_MESSAGE


@pytest.mark.django_db
def test_login_page(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_access_pages(client, setup_users):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    expected_url = reverse("login")
    assert response.url == expected_url
    # force to flash message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(LOGIN_REQUIRED_MESSAGE) > 0
    client.force_login(setup_users[0])
    response = client.get(reverse('logout'))
    assert response.status_code == 302
