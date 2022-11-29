# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import os




# data of clients company
class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, db_index=True)
    surname = models.CharField(max_length=80, db_index=True)
    birth = models.DateField(help_text='DD.MM.YYYY')
    email = models.EmailField(db_index=True, unique=True)
    # key = models.CharField("key for email tracking", max_length=255, default=os.urandom(5))
    seen_at = models.DateTimeField(null=True, blank=True)
    request = models.TextField(null=True, blank=True)


