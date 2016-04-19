from django.views.generic import View
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from liste_de_course.models import Liste

class HomeView(View):
    
    template_name='home.html'
    
    def get(self, request):
        
        # ajout des listes actives de l utilisateur au contexte pour les afficher sur la page d'accueil
        listes_actives = Liste.objects.filter(active=True) 
        
        return render(request, self.template_name,{'listes_actives':listes_actives})