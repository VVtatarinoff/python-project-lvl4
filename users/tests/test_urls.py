import pytest
from django.urls import reverse_lazy, reverse

from task_manager.mixins import LOGIN_REQUIRED_MESSAGE
from users.tests.conftest import NOLOGIN_PAGE, LOGIN_REQUIRED_PAGE_PK
from users.urls import urlpatterns


@pytest.mark.django_db
@pytest.mark.parametrize('page', NOLOGIN_PAGE)
def test_free_access_pages(client, page):
    response = client.get(reverse_lazy(page))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_access_pages(client, site_path, setup_users):
    response = client.get(site_path)
    assert response.status_code == 302
    expected_url = reverse("login")
    assert response.url == expected_url
    # force to flash message
    response = client.get(response.url)
    content = response.rendered_content
    assert content.find(LOGIN_REQUIRED_MESSAGE) > 0
    client.force_login(setup_users[0])
    response = client.get(site_path)
    assert response.status_code == 200


def test_coverage():
    paths_tested = len(
        NOLOGIN_PAGE | LOGIN_REQUIRED_PAGE_PK)
    paths_patterns = len(urlpatterns)
    assert paths_patterns == paths_tested
