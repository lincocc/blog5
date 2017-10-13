from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='detail'),
    url(r'^tag/$', views.TagView.as_view(), name='tag'),
    url(r'^category/$', views.CategoryView.as_view(), name='category'),
    url(r'^archive/$', views.ArchiveView.as_view(), name='archive'),
]
