#!/usr/bin/env python
# -*-coding:utf-8 -*-
# author：feng time:2019/1/28

from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()  # 只接受合法的邮件地址
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)  # charfield默认是<input type="text">html元素，这里用Textarea
                                                       # 来表示是一个<textarea>html元素，而不是默认的<input>元素


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 这里告诉django我们要创建表格的模型名称，它会自动为我们创建（因为继承了这个类的原因）
        fields = ('name', 'email', 'body')  # 用一个列表fields告诉django我们希望包含的表单字段，默认为所有的模型
        # 字段创建表单字段


class SearchForm(forms.Form):
    query = forms.CharField()
