from django.conf.urls import url

from .views import FichierList, FichierDetail, FichierCreate, FichierUpdate, FichierDelete

urlpatterns = [
    url(r'^g_$', FichierList.as_view(), name='fichier-list'),
    url(r'^g_(?P<pk>\d+)/$', FichierDetail.as_view(), name='fichier-detail'),
    url(r'^g_create/$', FichierCreate.as_view(), name='fichier-create'),
    url(r'^g_maj/(?P<pk>\d+)/$', FichierUpdate.as_view(), name='fichier-update'),
    url(r'^g_delete/(?P<pk>\d+)/$', FichierDelete.as_view(), name='fichier-delete'),
]
