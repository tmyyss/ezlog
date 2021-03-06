# coding=utf-8
from django.contrib import admin
from django import forms
from django.conf import settings

from blog.models import *
from blog.forms import *

class EntryInline(admin.StackedInline):
    model = Entry
    form = EntryForm

class CategoryAdmin(admin.ModelAdmin):
    inlines = [EntryInline]

class EntryAdmin(admin.ModelAdmin):
    form = EntryForm
    fields = ('title', 'category', 'tags', 'public', 'content',)
    list_display = ('title', 'category', 'author', 'created', 'modified', 'public')
    list_filter = ('created', 'modified', 'public', 'category')
    date_hierarchy = 'created'
    #filter_horizontal = ('tags',)
    search_fields = ('title', 'content')
    actions = ['make_publish', 'make_private']

    def save_model(self, request, obj, form, change):
        '''通过admin界面添加文章时, 自动把作者设为当前用户'''
        if not change:
            obj.author = request.user
        obj.save()

    def make_publish(self, request, queryset):
        queryset.update(public=True)
    make_publish.short_description = u'开放所选文章'
        
    def make_private(self, request, queryset):
        queryset.update(public=False)
    make_private.short_description = u'取消开放所选文章'

    class Media:
        js = ('admin/js/blog/article_edit.js',) + \
                settings.MEDIA_FOR_POST_EDITOR[settings.MARKUP_LANGUAGE]['js']

        css = {
            'all': ('admin/article_page_fix.css',) + \
                settings.MEDIA_FOR_POST_EDITOR[settings.MARKUP_LANGUAGE]['css']
        }

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
