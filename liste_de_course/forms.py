from django.forms import ModelForm

from .models import Article, Liste

class ArticleCreateForm(ModelForm):
    class Meta:
        model = Article
        fields = ['nom','rayon','marque','categorie']

class ListeCreateForm(ModelForm):
    class Meta:
        model = Liste
        fields = ['nom','magasin']