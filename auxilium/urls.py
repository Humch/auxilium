# a supprimer en prod
from django.conf import settings
from django.conf.urls.static import static
# ------------------------------------------

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import TemplateView

from liste_de_course import urls

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^$', login_required(TemplateView.as_view(template_name="base.html"))),
    url(r'^a/', include('liste_de_course.urls')),
    url(r'^admin/', admin.site.urls),
]

# a supprimer en prod

if settings.DEBUG:
    
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ------------------------------------------

