from django.test import TestCase
from django.urls import resolve


class HomeViewTest(TestCase):

    def test_index(self):
        """Ensure main url is connected to the jobbergate.views.home view"""
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'jobbergate.views.home')
