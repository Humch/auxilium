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

from django.contrib.auth.models import User

chemin = 'data'

def creer_liste(nom):
    
    proprietaire = User.objects.get(pk=1)
    
    magasin = Magasin.objects.get(pk=1)
    
    liste, created = Liste.objects.get_or_create(nom = nom, par_defaut = False, active = False, archive = True, propriete_de = proprietaire, magasin = magasin)
    
    if created:
        
        print('liste ajouté :  %s' % liste)
    
    else:
        
        print('liste existe déjà :  %s' % liste)
    
    return liste

def creer_rayon(nom):
    
    rayon, created = Rayon.objects.get_or_create(nom = nom)
                
    if created:
        
        print('rayon ajouté :  %s' % rayon)
    
    else:
        
        print('rayon existe déjà :  %s' % rayon)
    
    return rayon

def creer_categorie(nom):

    categorie, created = Categorie.objects.get_or_create(nom = nom)
                
    if created:
        
        print('categorie ajouté :  %s' % categorie)
    
    else:
        
        print('categorie existe déjà :  %s' % categorie)
    
    return categorie

def creer_marque(nom_article):
    
    nom = ''
    for w in nom_article.split(' '):
        
        try:
            if w[0].isupper():
            
                nom += w
            
        except:
            pass

    marque, created = Marque.objects.get_or_create(nom = nom)
                
    if created:
        
        print('marque ajouté :  %s' % marque)
    
    else:
        
        print('marque existe déjà :  %s' % marque)
        
    return marque

def creer_article(nom,rayon,categorie,marque):
    
    article, created = Article.objects.get_or_create(nom = nom, rayon = rayon, marque = marque)

    if created:
        article.categorie.add(categorie)
    
        article.save()
        
        print('article ajouté :  %s' % article)
    
    else:
        
        print('article existe déjà :  %s' % article)
        
    return article

def creer_produit(article,quantite,liste):
    
    print ('%s : %s de %s' % (article,quantite,liste))
    
    produit, created = Produit.objects.get_or_create(nom = article, quantite = quantite)
    
    liste.produit.add(produit)
    liste.save()
    
    return produit
        

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
            
            date = soup.find('font',attrs={"style":"color:#de0b1e"}).contents
            
            print(date[0])
            
            liste  = creer_liste(date[0])
            
            for produit,quantite in zip(produits,quantites):
                
                print('-->' + produit.contents[0] + ' : ' + quantite.contents[0])
    
                rayon = creer_rayon(tab_rayon[0])
                    
                categorie = creer_categorie(tab_rayon[0])
                
                marque = creer_marque(produit.contents[0])
                
                article = creer_article(produit.contents[0],rayon,categorie,marque)
                
                creer_produit(article,quantite.contents[0],liste)
    
if __name__ == '__main__':
    
    import_liste()