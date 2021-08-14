from django.test import TestCase
from django.urls import resolve
from .views import *
from django.http import HttpRequest

class HomePageTest(TestCase):


    def test_home_page_returns_correct_html(self):
        # request = HttpRequest()
        # response = index(request)
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'index.html')