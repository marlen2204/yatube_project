from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    text = 'Информация на главной странице'
    context ={
        'text': text,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    text = 'Информация о группах'
    context = {
        'text': text,
    }
    return render(request, template, context)
