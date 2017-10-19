from django.contrib.syndication.views import Feed

from blog.models import Post


class LatestPostFeed(Feed):
    title = 'Latest Posts'
    link = '/blog/'
    description = 'Latest Posts'

    def items(self):
        return Post.objects.all()[:4]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()
