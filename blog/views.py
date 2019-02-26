# -*-coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm
from haystack.query import SearchQuerySet

# Create your views here


def post_list(request, tag_slug=None):
    object_list = Post.published.all()  # published时自定义的manager,这里用来取回所有的Post
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # 用给定的tag_slug 得到tag_object
        print(object_list)
        object_list = object_list.filter(tags__in=[tag])  # 根据给定tags过滤，多对多关系
        print(object_list)

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')   # 得到请求的页面数
    try:
        posts = paginator.page(page)  # paginator.page(num),跳转num数值指代的页面
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)   # paginator.unm_pages返回页面数量
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)  # 返回具体的post
    # List of active comments for this post, 取回所有actives为true的comments
    comments = post.comments.filter(active=True)  # post.comments 这里comments即在models里定义的关系名称（related_name）
    new_comment = False

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet，在保存前需要对表单实例进行
            # 修改时commit = False 特别有用，save() 对ModelForm实例有效，对Form实例无效，因为
            # 它没有联系上任何model
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)  # 取回该post所有的tag的id
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # 取回包含这些tags的所有的post，除了该post
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # 数similar_posts中每个post多少个tag赋给same_tags，再将similar_posts按两个变量排序
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'new_comment': new_comment,
                   'similar_posts': similar_posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':  # 提交请求使用post方法
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data  # 如果数据有效，取回数据，数据是一个字典类型
            # ...send email
            post_url = request.build_absolute_uri(post.get_absolute_url())  # 获得完全的url包括http框架和主机名
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'],
                                                                     cd['comments'])
            send_mail(subject, message, '1491035393@qq.com',
                      [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


def post_search(request):
    form = SearchForm()
    cd = None
    results = None
    total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
                        .filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results}
                      )
