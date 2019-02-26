#!/usr/bin/env python
# -*-coding:utf-8 -*-
# author：feng time:2019/2/2

from django import template

register = template.Library()

from ..models import Post


@register.simple_tag()   # 修饰器,注册标签
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')  # 规定必须被从latest_posts.html中返回的数据渲染
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]  # 举出给定数目的由时间排列的posts
    return {'latest_posts': latest_posts}


from django.db.models import Count


@register.assignment_tag()
def get_most_commented_posts(count=5):
    # 取回评论数在前排的post
    return Post.published.annotate(total_comments=Count('comments'
                                                        )).order_by('-total_comments')[:count]


from django.utils.safestring import mark_safe
import markdown


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
