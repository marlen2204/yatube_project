from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        labels = {
            'group': _('Группа'),
            'text': _('Текст поста'),
        }
        help_texts = {
            'group': _('Введите название группы'),
            'text': _('Введите текст поста'),
        }
