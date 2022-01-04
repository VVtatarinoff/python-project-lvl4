from django import test
from django.urls import reverse_lazy


class URLTests(test.TestCase):
    PAGES_FREE_ACCESS = ['home', 'users', 'login', 'registration']
    PAGES_LOGIN_ACCESS = ['statuses', 'labels', 'tasks']

    def test_free_access(self):
        for page in self.PAGES_FREE_ACCESS:
            response = self.client.get(reverse_lazy(page))
            self.assertEqual(response.status_code, 200)

    def test_login_access(self):
        for page in self.PAGES_LOGIN_ACCESS:
            response = self.client.get(reverse_lazy(page))
            self.assertEqual(response.status_code, 302)
            expected_url = f'{reverse_lazy("home")}?next={reverse_lazy(page)}'
            self.assertEqual(response.url, expected_url)
