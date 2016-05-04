from django.forms import ModelForm, TextInput, ModelChoiceField, ModelMultipleChoiceField

from .models import Article, Rayon, Marque, Categorie, Liste, Magasin

class ArticleCreateForm(ModelForm):
    
    rayon = ModelChoiceField(
                queryset = Rayon.objects.all(),
                required = True,
                empty_label='Choix du rayon',
                label = ''
            )
    
    marque = ModelChoiceField(
                required = True,
                queryset = Marque.objects.all(),
                empty_label="Marque de l'article",
                label = ''
            )

    categorie = ModelMultipleChoiceField(
                queryset = Categorie.objects.all(),
                required = True
            )
    
    
    class Meta:
        model = Article
        fields = ['nom','rayon','marque','categorie']
        labels = {
            'nom': '',
        }
        widgets = {
            'nom': TextInput(
                attrs = {'required': True, 'placeholder': "Nom de l'article"}
            )
        }

class ListeCreateForm(ModelForm):
    magasin = ModelChoiceField(
                queryset = Magasin.objects.all(),
                required = True,
                empty_label='Choix du magasin',
                label = ''
            )
    
    class Meta:
        model = Liste
        fields = ['nom','magasin']
        labels = {
            'nom': '',
        }
        widgets = {
            'nom': TextInput(
                attrs = {'required': True, 'placeholder': 'Nom de la liste'}
            )
        }