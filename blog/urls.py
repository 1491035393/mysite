#!/usr/bin/env python
# -*-coding:utf-8 -*-
# author：feng time:2019/1/26
from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),  # ^和$是正则表达式的内容，功能是识别（筛选）url
    # url(r'^$',views.PostListView.as_view(),name = 'post_list'),  # 使用基于类的视图
    url(r'tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name="post_list_by_tag"),
    # url传参的例子:
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),  # year要求4个digital，month要求2个，day要求2个，post可以由单词和字符串组成
    url(r'^(?P<post_id>\d+)/share/$',views.post_share,
        name='post_share'),
]