from ..models import Post
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Name')

        cls.post = Post.objects.create(
            text='тестовый пост',
            author=cls.user,
        )

    def setUp(self):
        self.authorised_client = Client()
        self.authorised_client.force_login(self.user)

    def test_correct_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'тестовый пос',
        }
        response = self.authorised_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     kwargs={'username': 'Name'}))
        self.assertTrue(
            Post.objects.filter(
                text='тестовый пост',
                author=self.user,
            ).exists()
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_correct_edit_post(self):
        form_data = {
            'text': 'тестовый посt',
        }
        post_old = self.post.text
        self.authorised_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}),
            data=form_data)
        post_new = Post.objects.get(pk=self.post.pk)
        self.assertNotEqual(post_old, post_new)

