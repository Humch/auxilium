from bs4 import BeautifulSoup

import sys
import os

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

fichiers = [f for f in listdir(chemin) if isfile(join(chemin, f))]

print(fichiers)

for fichier in fichiers:
    
    with open(join(chemin, fichier)) as f:
        soup = BeautifulSoup(f.read(),'html.parser')
        
    for table in soup.find_all('table',attrs={'class':'deviceWidth tabRayon'}):
        
        rayon = table.find('font',attrs={'style':'text-transform:uppercase'}).contents
        print(rayon[0])
        produits = table.find_all('td',attrs={'width':'61%','style':'font-family:Arial, Helvetica, sans-serif; color:#2a2121; font-size:11px; padding-left:10px','class':'designation'})
        quantites = table.find_all('td',attrs={'width':'12%','style':'font-family:Arial, Helvetica, sans-serif; color:#2a2121; font-size:11px; text-align:center','class':"quantite"})
        
        for produit,quantite in zip(produits,quantites):
            print('-->' + produit.contents[0] + ' : ' + quantite.contents[0])
            
if __name__ == '__main__':
    
    pass