#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Tag, Attachment, AppSettings, WebSiteAbout
from blog.modelAdmin import CategoryAdmin, SettingsAdmin, WebSiteAboutAdmin

admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(AppSettings, SettingsAdmin)
admin.site.register(WebSiteAbout, WebSiteAboutAdmin)