from django.db import models
from django.contrib.auth.models import User

from pygments import formatters, highlight, lexers

from calcifer.common.models import Tag
from calcifer.snippets import managers

import datetime


class Language(models.Model):# {{{
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    language_code = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)

    # Manager
    objects = managers.LanguageManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('calcifer-language-detail', (), {'slug': self.slug})

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)
# }}}
class Snippet(models.Model): # {{{
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language)
    author = models.ForeignKey(User)
    description = models.TextField()
    code = models.TextField()
    highligted_code = models.TextField(editable=False)
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title

    def highlight(self):
        return highlight(self.code, self.language.get_lexer(),
                         formatters.HtmlFormatter(linenos=True))
        # linenos: generate the output with line numbers

    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.highligted_code = self.highlight()
        super(Snippet, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('calcifer-snippet-detail', (), {'object_id': self.id})
# }}}

