import random

import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from blog.models import Post, Tag, Category
from web import settings


def fake_data():
    Tag.objects.all().delete()
    Category.objects.all().delete()
    Post.objects.all().delete()

    user = User.objects.all().first()

    tag = ('django', 'python', 'java', 'javascript', 'css', 'html', 'web', 'app')
    tags = []
    for t in tag:
        tags.append(Tag.objects.create(name=t))

    def random_tags():
        return random.sample(tags, random.randint(1, 5))

    category = ('python教程', 'django教程', 'android教程', 'java教程')
    categories = []
    for c in category:
        categories.append(Category.objects.create(name=c))

    def random_category():
        return random.choice(categories)

    def random_datetime():
        return datetime.datetime(random.randint(2015, 2017),  # year
                                 random.randint(1, 12),  # month
                                 random.randint(1, 28),  # day
                                 random.randint(0, 23),  # hour
                                 random.randint(0, 59),  # min
                                 random.randint(0, 59),  # sec
                                 random.randint(0, 100),  # microsecond
                                 timezone.utc if settings.USE_TZ else None)

    for i in range(0, 100):
        post = Post.objects.create(title="title %s" % i, excerpt="summary %s" % i, body="content %s" % i,
                                   author=user, category=random_category(), created_time=random_datetime())
        post.tags.add(*random_tags())


class Command(BaseCommand):
    help = 'Import init data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        fake_data()
        self.stdout.write(self.style.SUCCESS('end import'))
