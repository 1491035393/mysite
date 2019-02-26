#!/usr/bin/env python
# -*-coding:utf-8 -*-
# author：feng time:2019/2/23

from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'  # 改变频率
    priority = 0.9

    def items(self):
        # 取回所有post
        return Post.published.all()

    def lastmod(self,obj):
        # 取回上次修改时间
        return obj.publish
