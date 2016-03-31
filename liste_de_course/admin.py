from django.contrib import admin

from .models import Magasin, Rayon, Marque, Categorie, Article,Produit, Liste

class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ('nom','marque')

admin.site.register(Magasin)
admin.site.register(Rayon)
admin.site.register(Marque)
admin.site.register(Categorie)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Produit)
admin.site.register(Liste)

