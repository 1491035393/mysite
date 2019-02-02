# -*-coding:utf-8 -*-
from django.contrib import admin
from .models import Post
from .models import Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    """display格式设置"""
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']


admin.site.register(Post, PostAdmin)  # 注册模型Post,使之能出现在管理界面,并且以继承于ModelAdmin的
                                    # postadmin风格展示


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)