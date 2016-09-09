from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Fichier

class FichierList(ListView):
    
    model = Fichier

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierList, self).dispatch(*args, **kwargs)
    
class FichierDetail(DetailView):

    model = Fichier

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FichierDetail, self).dispatch(*args, **kwargs)