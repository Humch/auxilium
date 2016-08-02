from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from liste_de_course.models import Article, Marque, Rayon, Categorie, Liste, Produit, Magasin

class MagasinTestCase(TestCase):
    
    def create_magasin(self, nom = 'YouhouMarché'):
        
        image = SimpleUploadedFile(name='test_image.jpg', content=open('liste_de_course/tests/test_image.jpg', 'rb').read(), content_type='image/jpeg')
        
        return Magasin.objects.create(nom = nom, logo = image )
        
    def test_create_magasin(self):
        
        m = self.create_magasin()
        self.assertTrue(isinstance(m, Magasin))
        self.assertEqual(m.__str__(), m.nom)

class RayonTestCase(TestCase):
    
    def create_rayon(self, nom = 'rayon pokémon'):

        return Rayon.objects.create(nom = nom)
        
    def test_create_rayon(self):
        
        r = self.create_rayon()
        self.assertTrue(isinstance(r, Rayon))
        self.assertEqual(r.__str__(), r.nom)
        
class MarqueTestCase(TestCase):
    
    def create_marque(self, nom = 'ACME'):

        return Marque.objects.create(nom = nom)
        
    def test_create_marque(self):
        
        m = self.create_marque()
        self.assertTrue(isinstance(m, Marque))
        self.assertEqual(m.__str__(), m.nom)
        
class CategorieTestCase(TestCase):
    
    def create_categorie(self, nom = 'Savannah'):

        return Categorie.objects.create(nom = nom)
        
    def test_create_categorie(self):
        
        c = self.create_categorie()
        self.assertTrue(isinstance(c, Categorie))
        self.assertEqual(c.__str__(), c.nom)
        
class ArticleTestCase(TestCase):
    
    def create_article(self, nom = 'roti de Pikachu', rayon = 'rayon pokémon', marque = 'ACME'):
        
        r = Rayon.objects.create(nom = nom)
        m = Marque.objects.create(nom = nom)

        return Article.objects.create(nom = nom, rayon = r, marque = m)
        
    def test_create_article(self):
        
        a = self.create_article()
        self.assertTrue(isinstance(a, Article))
        self.assertEqual(a.__str__(), a.nom)

class ProduitTestCase(TestCase):
    
    def create_produit_default_unit(self, quantite=3):
        
        r = Rayon.objects.create(nom = 'rayon pokémon')
        m = Marque.objects.create(nom = 'ACME')
        a = Article.objects.create(nom = 'roti de Pikachu', rayon = r, marque = m)
        
        return Produit.objects.create(nom = a, quantite = quantite)

    def test_create_produit_default_unit(self):
        
        p_d_u = self.create_produit_default_unit()
        self.assertTrue(isinstance(p_d_u, Produit))
        self.assertEqual(p_d_u.__str__(), p_d_u.nom.nom)
        self.assertEqual(p_d_u.unite, 'U')

    def create_produit(self, quantite=3, unite = 'pack'):
        
        r = Rayon.objects.create(nom = 'rayon pokémon')
        m = Marque.objects.create(nom = 'ACME')
        a = Article.objects.create(nom = 'roti de Pikachu', rayon = r, marque = m)
        
        return Produit.objects.create(nom = a, quantite = quantite, unite = unite)
    
    def test_create_produit(self):
        
        p = self.create_produit()
        self.assertTrue(isinstance(p, Produit))
        self.assertEqual(p.__str__(), p.nom.nom)
        self.assertEqual(p.unite, 'pack')
    
    