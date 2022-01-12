from django.urls import reverse_lazy, reverse
import pytest

from task_manager.test.conftest import NOLOGIN_PAGE, LOGIN_REQUIRED_PAGE
from task_manager.test.conftest import LOGIN_REQUIRED_PAGE_PK
from task_manager.urls import urlpatterns
from task_manager.views.constants import FLASH_LOGINREQUIRED


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
    assert content.find(FLASH_LOGINREQUIRED) > 0
    client.force_login(setup_users[0])
    response = client.get(site_path)
    assert response.status_code == 200


def test_coverage():
    paths_tested = len(
        NOLOGIN_PAGE | LOGIN_REQUIRED_PAGE | LOGIN_REQUIRED_PAGE_PK)
    paths_patterns = len(urlpatterns)
    ''' Admin and logout excluded from test'''
    assert paths_patterns - 2 == paths_tested
