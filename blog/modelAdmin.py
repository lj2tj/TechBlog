#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'comment',)
    search_fields = ('name',)

class WebSiteAboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'comment',)
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display',)
    search_fields = ('name',)