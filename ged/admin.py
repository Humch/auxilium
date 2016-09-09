from django.contrib import admin

from .models import Emetteur, Etiquette, Fichier

admin.site.register(Emetteur)
admin.site.register(Etiquette)
admin.site.register(Fichier)