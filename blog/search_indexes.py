#!/usr/bin/env python
# -*-coding:utf-8 -*-
# author：feng time:2019/2/23

from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr='publish')

    def get_model(self):
        # 返回完整post以便渲染使用
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()