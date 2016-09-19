from django.forms import ModelForm, FileInput, FileField
from django import forms

from .models import Fichier, Etiquette, Emetteur

class FichierUpdateForm(ModelForm):
    
    fichier = forms.FileField(
                    required=False,
                    widget = FileInput()
                )
    
    class Meta:
        
        model = Fichier
        fields = ['fichier','nom_fichier','emetteur','destinataire','date_document','etiquette']

        