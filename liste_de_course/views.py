from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse_lazy

import json

from django.http import HttpResponse

from .models import Article

class ArticleList(ListView):
    
    model = Article
    paginate_by = 25
    
class ArticleDetail(DetailView):

    model = Article
    
    context_object_name = "article"
    
    def get_context_data(self, **kwargs):
        
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['categorie'] = context['article'].categorie.all()
        
        return context
    
class ArticleCreate(CreateView):
    model = Article
    fields = ['nom','rayon','marque','categorie']

class ArticleUpdate(UpdateView):
    model = Article
    fields = ['nom','rayon','marque','categorie']

class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')
    
def get_article(request, **kwargs):
    
    if request.is_ajax():
    
        q = request.GET.get('term', '')
        articles = Article.objects.filter(nom__icontains = q )[:20]
        results = []
    
        for article in articles:
            article_json = {}
            article_json['value'] = '/a/%s/' % article.id
            article_json['label'] = '%s' % article.nom
            results.append(article_json)
        data = json.dumps(results)
    
    else:
        data = 'fail'
    
    mimetype = 'application/json'
    
    return HttpResponse(data, mimetype)

def add_to_list(request,**kwargs):
    pass
