from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

import json

from .models import Article, Liste, Produit, Categorie, Rayon

from .forms import AddArticleToListForm, ListeCreateForm

# Mixin pour la gestion des formulaires envoyés par AJAX --> issu du site Django https://docs.djangoproject.com/fr/1.9/topics/class-based-views/generic-editing/

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'nom': self.object.nom,
            }
            return JsonResponse(data)
        else:
            return response

# Vues concernant les articles (vue,edition,suppression)

class ArticleList(ListView):
    
    model = Article
    paginate_by = 10

    def get_context_data(self, **kwargs):
        
        context = super(ArticleList, self).get_context_data(**kwargs)
        
        # ajout de la categorie filtré pour le gérer dans la pagination
        
        context['cat'] = self.request.GET.get("categorie")
        context['ray'] = self.request.GET.get("rayon")
        context['art'] = self.request.GET.get("art")
        
        # ajout des catégories au contexte pour filtrer les catégories par requete GET
        context['all_categorie'] = Categorie.objects.all()
        context['all_rayon'] = Rayon.objects.all()
        
        # ajout des listes actives de l utilisateur au contexte pour l ajout à une liste
        context['liste'] = Liste.objects.filter(archive=False)
        
        # ajout du rayon pour afficher son nom si il ya un filtrage par rayon
        if self.request.GET.get("rayon"):
        
            context['rayon_id'] = Rayon.objects.get(id=self.request.GET.get("rayon"))
        
        return context

    def get_queryset(self):
        
        queryset = Article.objects.all().order_by('nom')

        if self.request.GET.get("categorie"):
            queryset = queryset.filter(categorie = self.request.GET["categorie"])
        
        if self.request.GET.get("art"):
            queryset = queryset.filter(nom__icontains = self.request.GET["art"])
        
        if self.request.GET.get("rayon"):
            queryset = queryset.filter(rayon = self.request.GET["rayon"])
        
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
    
class ArticleCreate(AjaxableResponseMixin, CreateView):
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

class ArticleForListUpdate(UpdateView):
    model = Article
    fields = ['nom','rayon','marque','categorie']
    template_name='liste_de_course/article_l_form.html'
    success_url = reverse_lazy('article-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleForListUpdate, self).dispatch(*args, **kwargs)
    
class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDelete, self).dispatch(*args, **kwargs)

# Vues concernant les listes (vues, edition, suppression)
    
class ListeList(ListView):
    
    model = Liste
    queryset = Liste.objects.all().order_by('archive','-date_creation_liste','-date_modification_liste')
    
    def get_context_data(self, *args, **kwargs):
        
        context = super(ListeList, self).get_context_data(**kwargs)
        context['form_liste'] = ListeCreateForm(user=self.request.user)
        
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
        context['addarticle2list'] = AddArticleToListForm()
        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeDetail, self).dispatch(*args, **kwargs)
    
class ListeCreate(AjaxableResponseMixin, CreateView):
    model = Liste
    fields = ['nom','active','archive','magasin','propriete_de']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeCreate, self).dispatch(*args, **kwargs)
    
class ListeUpdate(AjaxableResponseMixin, UpdateView):
    model = Liste
    fields = ['nom','magasin']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeUpdate, self).dispatch(*args, **kwargs)

class ListeForListUpdate(AjaxableResponseMixin, UpdateView):
    model = Liste
    fields = ['nom','magasin']
    template_name='liste_de_course/liste_l_form.html'
    success_url = reverse_lazy('liste-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListeForListUpdate, self).dispatch(*args, **kwargs)
    
class ListeDelete(DeleteView):
    model = Liste
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
        data = []
    
        for article in articles:
            article_json = {}
            article_json['label'] = '%s' % article.nom
            article_json['id'] = '%s' % article.id
            article_json['value'] = '%s' % article.nom
            data.append(article_json)
            
        return JsonResponse(data, safe=False)
    
    else:
        data = json.dumps('fail')
    
        return HttpResponseBadRequest(data, 'application/json')
    
    

# AJAX - ajoute un article à une liste

@login_required
def add_to_list(request,**kwargs):
    
    if request.method == 'POST' and request.is_ajax():
        
        try:
            
            a = Article.objects.get(id=request.POST.get("article_id"))
        
        except ObjectDoesNotExist:
        
            return HttpResponseBadRequest()
        
        try:
            
            p =  Produit.objects.filter(liste=request.POST.get("liste_id")).get(nom__id=request.POST.get("article_id"))
         
        except ObjectDoesNotExist:
            
            p = Produit(nom=a,quantite=request.POST.get("quantite"))
            p.save()
            l = Liste.objects.get(id=request.POST.get("liste_id"))
            l.produit.add(p)
            
        else:
            
            p =  Produit.objects.filter(liste=request.POST.get("liste_id")).get(nom__id=request.POST.get("article_id"))
            p.quantite = p.quantite + int(request.POST.get("quantite"))
            p.save()
        
        data = json.dumps('success')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponseBadRequest(data, mimetype)
    
# formulaire d'archivage de liste

@login_required
def archive_list(request,**kwargs):
    
    if request.method == 'POST' and request.is_ajax():
        liste = Liste.objects.get(id=request.POST.get("liste_id"))
        
        results = {}
        
        if liste.active:
            
            liste.active = False
            liste.archive = True
            liste.save()
            results['state'] = 'archive'
         
        elif not liste.active:
            
            liste.active = True
            liste.archive = False
            liste.save()
            results['state'] = 'active'
        
        results['listeid'] = request.POST.get("liste_id")
        data = json.dumps(results)
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)

# AJAX - permet de modifier la quantité d'un produit sur une liste

@login_required
def modify_product_quantity(request,**kwargs):
    
    if request.method == 'POST' and request.is_ajax():

        produit = Produit.objects.get(id=request.POST.get("produit_id"))
        results = {}
        
        if request.POST.get("action") == "add":
            
            produit.quantite = produit.quantite + 1
            
            produit.save()
            
            results['state'] = 'updated'
            results['quantite'] = str(produit.quantite)
            results['produit_id'] = produit.id
            
        elif request.POST.get("action") == "soustract":
            
                produit.quantite = produit.quantite - 1
            
                produit.save()
                
                results['state'] = 'updated'
                results['quantite'] = str(produit.quantite)
                results['produit_id'] = produit.id
            
        elif request.POST.get("action") == "delete":
                
                results['produit_id'] = produit.id
                
                produit.delete()
                
                results['state'] = 'deleted'
                
        else:
        
            data = json.dumps('fail')
    
            mimetype = 'application/json'
    
            return HttpResponseBadRequest(data, mimetype)
        
        data = json.dumps(results)
    
        mimetype = 'application/json'
    
        return HttpResponse(data, mimetype)
    
    else:
        
        data = json.dumps('fail')
    
        mimetype = 'application/json'
    
        return HttpResponseBadRequest(data, mimetype)