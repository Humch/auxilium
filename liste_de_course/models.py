from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

class Magasin(models.Model):
    
    nom = models.CharField(max_length=200)
    logo = models.ImageField()
    
    def __str__(self):
        return self.nom

class Rayon(models.Model):
    
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom
    
class Marque(models.Model):
    
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom
    
class Categorie(models.Model):
    
    nom = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom

class Article(models.Model):
    
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    categorie = models.ManyToManyField(Categorie)
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})
    
class Produit(models.Model):
    
    UNITE = 'U'
    GRAMME = 'gr'
    KILOGRAMME = 'kg'
    PACK = 'pack'
    TYPES_UNITE = (
        (UNITE, 'unite'),
        (GRAMME, 'gramme'),
        (KILOGRAMME,'kilogramme'),
        (PACK, 'pack'),
    )
        
    nom = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=4, decimal_places=1)
    unite = models.CharField(max_length=30, choices=TYPES_UNITE, default=UNITE)
    
    def __str__(self):
        return str(self.nom)

class Liste(models.Model):
    
    nom = models.CharField(max_length=200)
    produit = models.ManyToManyField(Produit, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    active = models.BooleanField()
    archive = models.BooleanField()
    propriete_de = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proprietaire')
    partage_avec = models.ManyToManyField(User, blank=True, related_name='utilisateur')
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('liste-list')