from django.test import TestCase
from django.urls import resolve
from .views import *
from django.http import HttpRequest

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Частный репетитор</title>', html)
        # self.assertTrue(html.endswith('</html>'))