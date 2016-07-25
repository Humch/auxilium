from django.conf.urls import url

from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ListeList, ListeDetail, ListeCreate, ListeUpdate, ListeDelete, get_article, add_to_list, archive_list, modify_product_quantity

urlpatterns = [
    url(r'^a_$', ArticleList.as_view(), name='article-list'),
    url(r'^a_(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^a_add/$', ArticleCreate.as_view(), name='article-add'),
    url(r'^a_maj/(?P<pk>\d+)/$', ArticleUpdate.as_view(), name='article-update'),
    url(r'^a_delete/(?P<pk>\d+)/$', ArticleDelete.as_view(), name='article-delete'),
    url(r'^l_$', ListeList.as_view(), name='liste-list'),
    url(r'^l_(?P<pk>\d+)/$', ListeDetail.as_view(), name='liste-detail'),
    url(r'^l_add/$', ListeCreate.as_view(), name='liste-add'),
    url(r'^l_maj/(?P<pk>\d+)/$', ListeUpdate.as_view(), name='liste-update'),
    url(r'^l_delete/(?P<pk>\d+)/$', ListeDelete.as_view(), name='liste-delete'),
    url(r'^get_article/', get_article, name='get_article'),
    url(r'^add_to_list/', add_to_list, name='add_to_list'),
    url(r'^archive_list/', archive_list, name='archive_list'),
    url(r'^modify_product_quantity/',modify_product_quantity, name='modify_product_quantity'),
]
