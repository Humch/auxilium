from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse_lazy

import json

from django.http import HttpResponse

from .models import Article, Liste, Produit, Categorie

# Vues concernant les articles (vue,edition,suppression)

class ArticleList(ListView):
    
    model = Article
    paginate_by = 10

    def get_context_data(self, **kwargs):
        
        context = super(ArticleList, self).get_context_data(**kwargs)
        
        # ajout de la categorie filtré pour le gérer dans la pagination
        
        context['cat'] = self.request.GET.get("categorie")
        context['art'] = self.request.GET.get("art")
        
        # ajout des catégories au contexte pour filtrer les catégories par requete GET
        context['all_categorie'] = Categorie.objects.all()
        
        # ajout des listes actives de l utilisateur au contexte pour l ajout à une liste
        context['liste'] = Liste.objects.filter(archive=False) 
        
        return context

    def get_queryset(self):

        if self.request.GET.get("categorie") and self.request.GET.get("art"):
            queryset = Article.objects.filter(nom__icontains = self.request.GET["art"]).filter(categorie = self.request.GET["categorie"]).order_by('nom')
            
        elif self.request.GET.get("categorie"):
            queryset = Article.objects.filter(categorie = self.request.GET["categorie"]).order_by('nom')
        
        elif self.request.GET.get("art"):
            queryset = Article.objects.filter(nom__icontains = self.request.GET["art"]).order_by('nom')
            
        else:
            queryset = Article.objects.all().order_by('nom')
        
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleList, self).dispatch(*args, **kwargs)
   
class ArticleDetail(DetailView):

    model = Article
    
    context_object_name = "article"
    
    def get_context_data(self, **kwargs):
        
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['categorie'] = context['article'].categorie.all()
        context['liste'] = Liste.objects.filter(archive=False)
        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDetail, self).dispatch(*args, **kwargs)
    
class ArticleCreate(CreateView):
    model = Article
    fields = ['nom','rayon','marque','categorie']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(*args, **kwargs)
    
class ArticleUpdate(UpdateView):
    model = Article
    fields = ['nom','rayon','marque','categorie']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleUpdate, self).dispatch(*args, **kwargs)
    
class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDelete, self).dispatch(*args, **kwargs)

# Vues concernant les listes (vues, edition, suppression)
    
class ListeList(ListView):
    
    model = Liste
    queryset = Liste.objects.all().order_by('-date_creation_liste','-date_modification_liste')
    
    def get_context_data(self, **kwargs):
        
        context = super(ListeList, self).get_context_data(**kwargs)
        
        return context
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeList, self).dispatch(*args, **kwargs)
    
class ListeDetail(DetailView):

    model = Liste
    
    context_object_name = "liste"
    
    def get_context_data(self, **kwargs):
        
        context = super(ListeDetail, self).get_context_data(**kwargs)
        context['produit'] = context['liste'].produit.all()
        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeDetail, self).dispatch(*args, **kwargs)
    
class ListeCreate(CreateView):
    model = Liste
    fields = ['nom','active','archive','magasin','propriete_de']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeCreate, self).dispatch(*args, **kwargs)
    
class ListeUpdate(UpdateView):
    model = Liste
    fields = ['nom','active','archive','magasin','propriete_de']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeUpdate, self).dispatch(*args, **kwargs)
    
class ListeDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('liste-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeDelete, self).dispatch(*args, **kwargs)
    
# vue ajax autocompletion (barre de recherche)
    
@login_required    
def get_article(request, **kwargs):
    
    if request.is_ajax():
    
        q = request.GET.get('term', '')
        articles = Article.objects.filter(nom__icontains = q )[:10]
        results = []
    
        for article in articles:
            article_json = {}
            article_json['label'] = '%s' % article.nom
            article_json['id'] = '%s' % article.id
            article_json['value'] = '%s' % article.nom
            results.append(article_json)
        data = json.dumps(results)
    
    else:
        data = 'fail'
    
    mimetype = 'application/json'
    
    return HttpResponse(data, mimetype)

# vue ajax permettant d'ajouter un article à une liste

@login_required
def add_to_list(request,**kwargs):
    
    if request.method == 'POST' and request.is_ajax():

        a = Article.objects.get(id=request.POST.get("article_id"))
        p = Produit(nom=a,quantite=request.POST.get("quantite"))
        p.save()
        
        l = Liste.objects.get(id=request.POST.get("liste_id"))
        
        l.produit.add(p)
        
        data = json.dumps('success')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
