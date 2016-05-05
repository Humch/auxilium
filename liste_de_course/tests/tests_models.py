from django.test import TestCase

from liste_de_course.models import Article, Marque, Rayon, Categorie

class ArticleTestCase(TestCase):
    
    def setUp(self):
        Rayon.objects.create(nom='Bricolage')
        Marque.objects.create(nom='ACME')
        
    def test_articleSave(self):
        rayon = Rayon.objects.get(nom='Bricolage')
        marque = Marque.objects.get(nom='ACME')
        
        self.assertTrue(Article.objects.get_or_create(nom = 'roti de Pikachu',rayon = rayon,marque = marque))