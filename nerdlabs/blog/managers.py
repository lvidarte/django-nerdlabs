from django.db import models
import datetime


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(
                status__gte=2,
                publish__lte=datetime.datetime.now())
