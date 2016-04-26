from django.views.generic import View
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from django.http import HttpResponse

import json

from liste_de_course.models import  Article, Rayon, Marque, Categorie, Liste, Magasin

from liste_de_course.forms import ArticleCreateForm, ListeCreateForm


class HomeView(View):
    
    template_name='home.html'
    
    def get(self, request):
        
        # ajout des listes actives de l utilisateur au contexte pour les afficher sur la page d'accueil
        listes_actives = Liste.objects.filter(active=True) 
        form_article = ArticleCreateForm()
        form_liste = ListeCreateForm()
        return render(request, self.template_name,{'listes_actives':listes_actives,'form_article':form_article,'form_liste':form_liste})
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

def create_article(request, **kwargs):
    
    if request.method == 'POST' and request.is_ajax():
        
        article = Article(nom = request.POST.get("nom"),marque = Marque.objects.get(pk = request.POST.get("marque")),rayon = Rayon.objects.get(pk = request.POST.get("rayon")))
        article.save()
        
        if request.POST.get("categorie"):
            for cat in request.POST.get("categorie"):
            
                article.categorie.add(cat)
        
        data = json.dumps(article.nom)
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
def create_liste(request, **kwargs):
    
    if request.method == 'POST' and request.is_ajax():
        
        liste = Liste(nom = request.POST.get("nom"),magasin = Magasin.objects.get(pk = request.POST.get("magasin")),propriete_de = request.user,active=True,archive=False)
        liste.save()
        
        data = json.dumps('success')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)