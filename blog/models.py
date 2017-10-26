from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '%s#%s' % (reverse('blog:category'), self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '%s#%s' % (reverse('blog:tag'), self.name)


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comments(MPTTModel):
    user = models.ForeignKey(User)
    content = models.TextField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    post = models.ForeignKey(Post)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['-created_time']

