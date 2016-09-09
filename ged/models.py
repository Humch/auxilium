from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from wand.image import Image

class Emetteur(models.Model):
    
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom

class Etiquette(models.Model):
    
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom

class Fichier(models.Model):
    
    fichier = models.FileField(upload_to='GED/')
    thumbnail = models.ImageField(upload_to='GED/thumb/',default='GED/thumb/default-fichier.jpg',blank=True)
    emetteur = models.ForeignKey(Emetteur, on_delete=models.CASCADE)
    etiquette = models.ManyToManyField(Etiquette,blank=True)
    date_creation = models.DateTimeField(auto_now_add = True)
    date_modification = models.DateTimeField(auto_now = True)
    date_document = models.DateField()
    propriete_de = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proprietaire_GED')
    partage_avec = models.ManyToManyField(User, blank=True, related_name='utilisateur_GED')

    def __str__(self):
        return self.fichier.name
    
# TODO ==> creer une methode post_save