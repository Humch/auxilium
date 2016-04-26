# a supprimer en prod
from django.conf import settings
from django.conf.urls.static import static
# ------------------------------------------

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import TemplateView

from .views import HomeView, create_article, create_liste

from liste_de_course import urls

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^$', HomeView.as_view()),
    url(r'^create_article/', create_article, name='create_article'),
    url(r'^create_liste/', create_liste, name='create_liste'),
    url(r'^a/', include('liste_de_course.urls')),
    url(r'^admin/', admin.site.urls),
]

# a supprimer en prod

if settings.DEBUG:
    
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ------------------------------------------

