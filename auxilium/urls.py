from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import TemplateView

from liste_de_course import urls

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^a/', include('liste_de_course.urls')),
    url(r'^admin/', admin.site.urls),
]
