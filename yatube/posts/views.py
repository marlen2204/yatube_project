from django.shortcuts import render, \
    get_object_or_404, redirect
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    # извлечение номера страницы
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def profile(request, username):
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, 10)
    # извлечение номера страницы
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    quantity = len(posts)
    context = {
        'page_obj': page_obj,
        'author': author,
        'quantity': quantity,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    author = User.objects.get(posts=post_id)
    post = get_object_or_404(Post, pk=post_id)
    quantity = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'quantity': quantity,
        'author': author,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    template = 'posts/create_post.html'
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect('posts:profile', post.author.username)
        return render(request, template, context)
    else:
        return render(request, template, context)



@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id == post.author.id:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post.author = request.user
                post.text = form.cleaned_data['text']
                post.group = form.cleaned_data['group']
                post.save()
                return redirect('posts:post_detail', post_id=post.id)

        else:
            form = PostForm(instance=post)
            context = {
                'form': form,
                'is_edit': True,
                'post_id': post_id

            }
        return render(request, 'posts/create_post.html', context)
    else:
        return redirect('index')
