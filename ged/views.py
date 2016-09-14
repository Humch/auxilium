from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.urlresolvers import reverse_lazy

import json

from .models import Fichier, Etiquette

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

class FichierList(ListView):
    
    model = Fichier
    context_object_name = 'fichiers'

    def get_context_data(self, **kwargs):
        
        context = super(FichierList, self).get_context_data(**kwargs)

        context['all_etiquette'] = Etiquette.objects.all()
        
        return context
    
    def get_template_names(self, **kwargs):
    
        if self.request.method == 'GET' and self.request.is_ajax():
        
            if self.request.GET.get("action") == "details":
        
                template_name = 'ged/fichier_list/details.html'
        
            elif self.request.GET.get("action") == "mosaique":
        
                template_name = 'ged/fichier_list/mosaique.html'
            
            elif self.request.GET.get("action") == "liste":
        
                template_name = 'ged/fichier_list/liste.html'
                
            self.request.session['vuefichier'] = template_name
            
        else:
            template_name = 'ged/fichier_list.html'
            
            if not 'vuefichier' in self.request.session:
                self.request.session['vuefichier'] = 'ged/fichier_list/mosaique.html'
            
        return template_name
    
    def get_queryset(self):
        
        queryset = Fichier.objects.all().filter(propriete_de=self.request.user)
        
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierList, self).dispatch(*args, **kwargs)
    
class FichierDetail(DetailView):

    model = Fichier
    
    def get_context_data(self, **kwargs):
        
        context = super(FichierDetail, self).get_context_data(**kwargs)

        context['all_etiquette'] = Etiquette.objects.all()
        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierDetail, self).dispatch(*args, **kwargs)

class FichierUpdate(AjaxableResponseMixin, UpdateView):
    model = Fichier
    fields = ['fichier','nom_fichier','emetteur','date_document','etiquette']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierUpdate, self).dispatch(*args, **kwargs)
    
class FichierDelete(AjaxableResponseMixin, DeleteView):
    model = Fichier
    success_url = reverse_lazy('fichier-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierDelete, self).dispatch(*args, **kwargs)