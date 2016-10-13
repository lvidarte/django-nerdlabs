"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.db import models
import datetime


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(
                status__gte=2,
                publish__lte=datetime.datetime.now())
