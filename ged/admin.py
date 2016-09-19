from django.contrib import admin

from .models import Emetteur,Destinataire, Etiquette, Fichier

admin.site.register(Emetteur)
admin.site.register(Destinataire)
admin.site.register(Etiquette)
admin.site.register(Fichier)