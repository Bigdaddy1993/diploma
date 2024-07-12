from django.test import TestCase
from django.urls import reverse

from blog.models import Blog
from users.models import User


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru",
            is_staff=True,
            is_active=True,
            is_superuser=True,
            password=12345
        )

        self.blog = Blog.objects.create(title="blog 1", body="testing",
                                        is_payment=True, views_count=2)

    def test_get_create_blog(self):
        new_blog = Blog.objects.create(title="test", body="test1",
                                       is_payment=True, views_count=1)

        self.assertEqual(new_blog.title, 'test')
        self.assertEqual(new_blog.body, 'test1')

    def test_get_list_blog(self):
        url = reverse("blog:blog_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_update_blog(self):
        self.blog.title = 'Lux'
        self.blog.body = 'Good boy'
        self.blog.save()
        self.assertEqual(self.blog.title, 'Lux')
        self.assertNotEqual(self.blog.body, 'testing')

    def test_get_delete_blog(self):
        self.blog.delete()
        self.assertEqual(Blog.objects.count(), 0)
