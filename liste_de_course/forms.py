from django.forms import ModelForm, TextInput, ModelChoiceField, ModelMultipleChoiceField, Select

from .models import Article, Rayon, Marque, Categorie, Liste, Magasin

class ArticleCreateForm(ModelForm):
    
    rayon = ModelChoiceField(
                queryset = Rayon.objects.all(),
                empty_label='Choix du rayon',
                label = '',
                widget = Select(attrs={'required':True})
            )
    
    marque = ModelChoiceField(
                queryset = Marque.objects.all(),
                empty_label="Marque de l'article",
                label = '',
                widget = Select(attrs={'required':True})
            )

    categorie = ModelMultipleChoiceField(
                queryset = Categorie.objects.all()
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
                empty_label='Choix du magasin',
                label = '',
                widget = Select(attrs={'required':True})
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