# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)  # title 标题，charfield在SQL数据库中是可变长度的字符串类型
    slug = models.SlugField(max_length=250,
                            unique_for_date= 'publish')  # slug用于创建友好的url，添加unique_for_date参数是为了创建url
                                                         # 时使用数据和slug
    author = models.ForeignKey(User,
                               related_name='blog_posts')  # ForeignKey用于定义多对一关系，
    body = models.TextField()  # the body of the post
    publish = models.DateTimeField(default=timezone.now)  # 发行时间
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated = models.DateTimeField(auto_now=True)  # 更新时间
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft') # post的状态
    objects = models.Manager()  # 默认manager
    published = PublishManager()  # 习惯的manager
    tags = TaggableManager()  # This tags manager will allow you to add, retrieve,and remove tags form post projects

    class Meta:
        ordering = ('-publish',)  # 用于查询数据库时能自动排序

    def __str__(self):
        """默认的可读representation"""
        return self.title

    def get_absolute_url(self):
        """返回指定格式的url"""
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),  # 取月数，带零形式
                             self.publish.strftime('%d'),  # 取天数，带领形式
                             self.slug
                             ])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')  # 通过外键联系单个post和创建的comment，多对一关系，
    # related_name允许我们命名从相关的对象到这个参量的关系，定义了这个之后我们可以通过post.comments.all()取回一个post
    # 所有的comment,也可以通过comment.post 取回一个comment 对应的post
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # 布尔类型值，用于手动操作使不合适的comments无效

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


