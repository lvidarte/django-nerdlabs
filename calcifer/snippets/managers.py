from django.db import models, connection


class LanguageManager(models.Manager):
    def top_languages(self):
        from cab.models import Snippet
        subquery = "SELECT COUNT(*) FROM %(snippets_table) WHERE %(snippets_table)s.%(language_column)s = cab_language.id"
        params = {'snippets_table': connection.ops.quote_name('language_id'), 'language_column': connection.ops.quote_name('language_id')}
        return self.extra(select={'score': subquery % params},
                          order_by=['score'])
