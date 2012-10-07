# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
#from django.shorcuts import get_object_or_404
#from django.http import HttpResponse
#from django.http import Http404
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.template import RequestContext

from calcifer.blog.models import Post
from calcifer.common.tools import search


def post_list(request, page=0, paginate_by=20, **kwargs):
    page_size = getattr(settings, 'BLOG_PAGESIZE', paginate_by)
    return list_detail.object_list(
        request,
        queryset=Post.objects.published(),
        paginate_by=page_size,
        page=page,
        **kwargs
    )
post_list.__doc__ = list_detail.object_list.__doc__


def post_detail(request, slug, year, month, day, **kwargs):
    """
    Displays post detail. If user is superuser, view will display 
    unpublished post detail for previewing purposes.
    """
    posts = None
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.published()

    return date_based.object_detail(
        request,
        year=year,
        month=month,
        month_format='%m',
        day=day,
        date_field='publish',
        slug=slug,
        queryset=posts,
        **kwargs
    )
post_detail.__doc__ = date_based.object_detail.__doc__


def post_archive(request):
    posts = Post.objects.published().order_by('-publish')
    return render_to_response('blog/post_archive.html', locals(),
                              context_instance=RequestContext(request))


def post_search(request):
    q = ""
    post_list = []
    word_list = []
    if request.GET:
        q = request.GET['q']
        word_list = search.strip_stop_words(q)
        if word_list:
            post_list = Post.objects.published().filter(
                            search.get_q(word_list, 'body', 'and') |
                            search.get_q(word_list, 'title', 'and'))

    return render_to_response('blog/post_search.html',
                              {'search_term': q,
                               'object_list': post_list,
                               'word_list': word_list},
                              context_instance=RequestContext(request))


def post_list_by_tag(request, slug, page=0, paginate_by=20, **kwargs):
    page_size = getattr(settings, 'BLOG_PAGESIZE', paginate_by)
    tag = Tag.objects.get(slug=slug)
    return list_detail.object_list(
        request,
        queryset=Post.objects.published().filter(tags__id=tag.id),
        paginate_by=page_size,
        page=page,
        extra_context={'tag': tag},
        **kwargs
    )
post_list_by_tag.__doc__ = list_detail.object_list.__doc__


def tag_cloud(request):
    tags = Tag.objects.all()
    return render_to_response('blog/tag_cloud.html', locals(),
                              context_instance=RequestContext(request))


