from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='imie_nazwisko',
            password='password',
        )

        self.post = Post.objects.create(
            title='Test title',
            content='text',
            author=self.test_user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test title')
        self.assertEqual(self.post.content, 'text')
        self.assertEqual(self.post.author.username, 'imie_nazwisko')

    def test_post_dates_auto_populated(self):
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.published_at)

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test title')