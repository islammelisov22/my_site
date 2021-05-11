from django.test import TestCase

from shop.models import Category


class TestCategory(TestCase):
    def test_create_category_success(self):
        payload = {
            'title': 'test_title'
        }
        category = Category.objects.create(**payload)
        self.assertEqual(category.title, payload['title'])

    def test_create_category_fail(self):
        payload = {
            'title': 'test_title',
            'unknown_field': 'value'
        }
        with self.assertRaises(TypeError):
            Category.objects.create(**payload)

    """
    Testing model updating function.
    """

    def test_update_category(self):
        new_title = 'new test title'
        payload = {
            'title': 'test_title',
        }
        category = Category.objects.create(**payload)
        category.title = new_title
        category.save()
        category.refresh_from_db()
        self.assertEqual(category.title, new_title)

    """
    Testing model deleting function.
    """

    def test_delete_category(self):
        payload = {
            'title': 'test_title',
        }
        category = Category.objects.create(**payload)
        pk = category.pk
        category.delete()
        with self.assertRaises(Category.DoesNotExist):
            category = Category.objects.get(pk=pk)
