from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from nerdlabs.blog.models import Post
from nerdlabs.common.models import Tag
from nerdlabs.common.tools import search


def post_list(request):
    posts_all = Post.published.all()
    paginator = Paginator(posts_all, settings.BLOG_PAGESIZE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'object_list': posts})


def post_detail(request, year, month, day, slug):
    if request.user.is_superuser:
        manager = Post.objects
    else:
        manager = Post.published
    post = get_object_or_404(manager,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    return render(request, 'blog/post_detail.html', {'object': post})


def post_archive(request):
    posts = Post.published.order_by('-publish')
    return render(request, 'blog/post_archive.html', {'posts': posts})


def post_search(request):
    q = ""
    post_list = []
    word_list = []
    if request.GET:
        q = request.GET['q']
        word_list = search.strip_stop_words(q)
        if word_list:
            post_list = Post.published.filter(
                    search.get_q(word_list, 'body', 'and') |
                    search.get_q(word_list, 'title', 'and'))
    return render(request, 'blog/post_search.html', {
            'search_term': q,
            'object_list': post_list,
            'word_list': word_list})


def post_list_by_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts_all = Post.published.filter(tags__id=tag.id)
    paginator = Paginator(posts_all, settings.BLOG_PAGESIZE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {
        'object_list': posts,
        'tag': tag})


def tag_cloud(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_cloud.html', {'tags': tags})

