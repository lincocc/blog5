from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'
