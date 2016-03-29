from bs4 import BeautifulSoup

import sys
import os
import logging

from os import listdir

from os.path import isfile, join

# Ajout des settings Django pour l'import

sys.path.append('/home/fabien/Projets/auxilium')

os.environ['DJANGO_SETTINGS_MODULE'] = 'auxilium.settings_dev'

import django

# setup Django pour intialiser les paramètres

django.setup()

from liste_de_course.models import Magasin, Rayon, Marque, Categorie, Article, Liste, Produit

chemin = 'data'

def creer_liste(nom):
    
    liste, created = Liste.objects.get_or_create(nom = nom)
    
    return liste

def creer_rayon(nom):
    
    rayon, created = Rayon.objects.get_or_create(nom = nom)
                
    if created:
        
        print('rayon ajouté :  %s' % rayon)
    
    else:
        
        print('rayon existe déjà :  %s' % rayon)
    
    return rayon, created

def creer_categorie(nom):

    categorie, created = Categorie.objects.get_or_create(nom = nom)
                
    if created:
        
        print('categorie ajouté :  %s' % categorie)
    
    else:
        
        print('categorie existe déjà :  %s' % categorie)
    
    return categorie, created

def creer_marque(nom):
    
    marque, created = Marque.objects.get_or_create(nom = nom)
                
    if created:
        
        print('marque ajouté :  %s' % marque)
    
    else:
        
        print('marque existe déjà :  %s' % marque)
        
    return marque, created

def creer_article(nom,rayon,categorie,marque):
    
    article, created = Article.objects.get_or_create(nom = nom, rayon = rayon, marque = marque)
    
    article.categorie.add(categorie)
    
    article.save()
    
    if created:
        
        print('article ajouté :  %s' % produit)
    
    else:
        
        print('existe déjà :  %s' % produit)
        
    return article,created

def creer_produit(article,quantite,liste):
    
    produit, created = Produit.objects.get_or_create(article = article, quantite = quantite)
    
    liste.produit.add(produit)
    liste.save()
    
    return produit, created
        

def import_liste():

    fichiers = [f for f in listdir(chemin) if isfile(join(chemin, f))]
    
    for fichier in fichiers:
        
        print('ouverture de :  %s' % fichier)
        
        with open(join(chemin, fichier)) as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            
        for table in soup.find_all('table',attrs={'class':'deviceWidth tabRayon'}):
            
            tab_rayon = table.find('font',attrs={'style':'text-transform:uppercase'}).contents
            
            print(tab_rayon[0])
            
            produits = table.find_all('td',attrs={'width':'61%','style':'font-family:Arial, Helvetica, sans-serif; color:#2a2121; font-size:11px; padding-left:10px','class':'designation'})
            quantites = table.find_all('td',attrs={'width':'12%','style':'font-family:Arial, Helvetica, sans-serif; color:#2a2121; font-size:11px; text-align:center','class':"quantite"})
            
            creer_liste()
            
            for produit,quantite in zip(produits,quantites):
                
                print('-->' + produit.contents[0] + ' : ' + quantite.contents[0])
    
                creer_rayon(tab_rayon[0])
                    
                creer_categorie(tab_rayon[0])
                
                creer_marque(produit.contents[0])
                
                creer_article(produit.contents[0],rayon,categorie,marque)
                
                creer_produit(article,quantite.contents[0],liste)
    
if __name__ == '__main__':
    
    import_liste()