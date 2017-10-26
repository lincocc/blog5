from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from blog.models import Post, Category, Tag, Comments

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comments, MPTTModelAdmin)
