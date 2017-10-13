from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Tag


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'


class TagView(ListView):
    # model = Tag
    context_object_name = 'tags'
    template_name = 'blog/tags.html'
    queryset = Tag.objects.annotate(post_num=Count('post')).filter(post_num__gt=0)


class CategoryView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/category.html'


class ArchiveView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/archive.html'
