from django.conf.urls import url

from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, get_article

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='article-list'),
    url(r'^(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^add/$', ArticleCreate.as_view(), name='article-add'),
    url(r'^maj/(?P<pk>\d+)/$', ArticleUpdate.as_view(), name='article-update'),
    url(r'^delete/(?P<pk>\d+)/$', ArticleDelete.as_view(), name='article-delete'),
    url(r'^get_article/', get_article, name='get_article'),
]
