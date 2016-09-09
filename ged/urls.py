from django.conf.urls import url

from .views import FichierList, FichierDetail

urlpatterns = [
    url(r'^g_$', FichierList.as_view(), name='fichier-list'),
    url(r'^g_(?P<pk>\d+)/$', FichierDetail.as_view(), name='fichier-detail'),
]
