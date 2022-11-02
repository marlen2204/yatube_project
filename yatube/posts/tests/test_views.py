from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, Group
from django import forms

User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')

        cls.group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.another_group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test_slug2',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='тестовый пост',
            author=cls.user,
            group=cls.group,
        )

        for i in range(13):
            cls.posts = Post.objects.create(
                text=f'test post {i}',
                author=cls.user,
                group=cls.group,
            )

    def setUp(self):
        self.authorised_client = Client()
        self.authorised_client.force_login(self.user)

    def test_view_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}):
                'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'NoName'}):
                'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorised_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def post_test(self, response):
        first_object = response.context['page_obj'][0]
        post_text = first_object.text
        post_author = first_object.author
        post_group = first_object.group
        self.assertEqual(post_text, 'тестовый пост')
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_group, self.group)

    def test_correct_context_index(self):
        response = self.authorised_client.get(reverse('posts:index'))
        self.post_test(response)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_index(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_correct_context_group_list(self):
        response = self.authorised_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}))
        self.post_test(response)
        group_obj = response.context['group']
        self.assertEqual(group_obj, self.group)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_group_list(self):
        response = self.client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_correct_context_profile(self):
        response = self.authorised_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'NoName'}))
        self.post_test(response)
        author_obj = response.context['author']
        self.assertEqual(author_obj, self.user)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_profile(self):
        response = self.client.get(
            reverse('posts:profile',
                    kwargs={'username': 'NoName'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_correct_context_post_detail(self):
        response = self.authorised_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}))
        post_obj = response.context['post']
        author_obg = response.context['author']
        self.assertEqual(post_obj, self.post)
        self.assertEqual(author_obg, self.user)

    def test_correct_context_create_post(self):
        response = self.authorised_client.get(
            reverse('posts:post_create'))
        form_field = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_field.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_correct_context_post_edit(self):
        response = self.authorised_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}))
        form_field = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_field.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

        is_edit_context = response.context['is_edit']
        post_id_context = response.context['post_id']
        self.assertEqual(is_edit_context, True)
        self.assertEqual(post_id_context, self.post.id)

    def test_correct_group_of_post(self):
        response = self.authorised_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug2'}))
        group_obj = response.context['page_obj']
        self.assertNotIn(self.post, group_obj)
