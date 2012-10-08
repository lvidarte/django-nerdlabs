# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from calcifer.blog.managers import PublicManager
from calcifer.common.models import Tag, File
from calcifer.common.tools import parser

import datetime

DRAFT_STATUS = 1
PUBLIC_STATUS = 2

STATUS_CHOICES = (
    (DRAFT_STATUS, _('Draft')),
    (PUBLIC_STATUS, _('Public')),
)

MARKDOWN_MARKUP = 1
REST_MARKUP = 2
TEXT_MARKUP = 3

MARKUP_CHOICES = (
    (MARKDOWN_MARKUP, _('Markdown')),
    (REST_MARKUP, _('reStructuredText')),
    (TEXT_MARKUP, _('Text')),
)


class PostFile(models.Model):
    post = models.ForeignKey('Post')
    file = models.ForeignKey(File)
    label = models.CharField(_('label'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('post file')
        verbose_name_plural = _('post files')
        db_table  = 'calcifer_blog_post_file'


class Post(models.Model):
    """Post model."""
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(_('body'), help_text=_("""
                        Media tags images: [[label]] [[label|size]]
                        Links: {{label}} {{label|text}}
                        Read more: [:more:]"""))
    markup = models.IntegerField(_('markup'), choices=MARKUP_CHOICES,
                                 default=MARKDOWN_MARKUP)
    status = models.IntegerField(_('status'),
                                 choices=STATUS_CHOICES, default=DRAFT_STATUS)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'),
                                   default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    files = models.ManyToManyField(File, blank=True, through='PostFile')

    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table  = 'calcifer_blog_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    def get_status(self):
        return True if self.status == 2 else False

    get_status.short_description = _('status')
    get_status.boolean = True
    get_status.admin_order_field = 'status'

    @models.permalink
    def get_absolute_url(self):
        return ('blog-post-detail', None, {
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_body_html(self, less=False):
        body = parser.parse_media_tags(self.id, self.body,
                                       self.files, self.markup)

        if self.markup == MARKDOWN_MARKUP:
            body = parser.markdown_to_html(body)
        elif self.markup == REST_MARKUP:
            body = parser.rest_to_html(body)
        elif self.markup == TEXT_MARKUP:
            body = parser.text_to_html(body) 

        if less:
            return parser.parse_tag_more(body, stop=True,
                                         link=self.get_absolute_url(),
                                         text_link=_('Read more'))
        else:
            return parser.parse_tag_more(body)

    def get_body_html_less(self):
        return self.get_body_html(less=True)

    def get_next_post(self):
        # @See http://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_next_by_FOO
        return self.get_next_by_publish(status__gte=2)

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)


