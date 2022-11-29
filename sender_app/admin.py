# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Clients


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'birth', 'email', 'seen_at')
    list_filter = ('birth', 'name', 'surname')


admin.site.register(Clients, ClientsAdmin)


