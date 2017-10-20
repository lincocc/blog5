from django import template
from django.db.models import Count

from blog.models import Post, Tag, Category

register = template.Library()


@register.simple_tag
def get_recent_post():
    return Post.objects.all()[:5]


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(post_num=Count('post')).filter(post_num__gt=0)


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_posts(num=None):
    return Post.objects.all()[:num]


@register.simple_tag
def get_most_read_post(num=5):
    return Post.objects.all().order_by('-views')[:num]


@register.simple_tag
def get_avatar_url(user):
    account = get_socialaccount(user)
    if account:
        return account.get_avatar_url()
    return 'https://getuikit.com/docs/images/avatar.jpg'


@register.simple_tag
def get_profile_url(user):
    account = get_socialaccount(user)
    if account:
        return account.get_profile_url()
    return '#'


def get_socialaccount(user):
    if hasattr(user, 'socialaccount_set'):
        return user.socialaccount_set.first()
    return None
