import markdown
import re
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView

from blog.forms import CommentForm
from blog.models import Post, Category, Tag, Comments


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 8


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        response = super(PostView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostView, self).get_object(queryset)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ], extension_configs={
            'markdown.extensions.toc': {
                'anchorlink': True,
                'baselevel': 3,
                'slugify': slugify
            },
        })
        post.body = md.convert(post.body)
        post.toc = md.toc
        post.comments = post.comments_set.all()
        return post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        form = CommentForm()
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            # if comment.parent is not None:
            #     comment.content, count = re.subn(r'^\[reply\].*?\[/reply\]', '', comment.content, 1)
            #     if not comment.content:
            #         return redirect(obj)
            #
            #     if count is 0:
            #         comment.parent = None

            comment.save()
        return redirect(obj)


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


class ProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context
