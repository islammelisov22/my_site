from django.test import TestCase
from django.urls import reverse


class HomePageViewTest(TestCase):
    def test_view_home_page_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_home_page_get(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base.html')
