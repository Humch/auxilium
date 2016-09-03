from django.views.generic import View
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from django.http import HttpResponse

from liste_de_course.models import  Article, Rayon, Marque, Categorie, Liste, Magasin

from liste_de_course.forms import ArticleCreateForm, ListeCreateForm


class HomeView(View):
    
    template_name='home.html'
    
    def get(self, request):
        
        # ajout des listes actives de l utilisateur au contexte pour les afficher sur la page d'accueil
        listes_actives = Liste.objects.filter(active=True) 
        form_article = ArticleCreateForm()
        form_liste = ListeCreateForm(user=request.user)
        
        return render(request, self.template_name,{'listes_actives':listes_actives,'form_article':form_article,'form_liste':form_liste})
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)