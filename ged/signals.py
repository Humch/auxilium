from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from .models import Fichier

import magic
from wand.image import Image
from os import remove

# génère un aperçu du fichier qui va remplacer le champ thumbnail par défaut

@receiver(post_save, sender=Fichier)
def generate_thumbnail(sender,instance, **kwargs):
    
    mime = magic.Magic(mime=True)
    type_fichier = mime.from_file(instance.fichier.path)
    nom_thumbnail = 'fichiers/' + instance.nom_fichier + '_thumb.jpeg'
    if instance.thumbnail.name == 'GED/thumb/default-fichier.jpg':

        if type_fichier == 'image/png' or type_fichier == 'image/jpeg':

            with Image(filename=instance.fichier.path) as img:
                with img.clone() as converted:
                    converted.format = 'jpeg'
                    converted.resize(300,400)
                    converted.save(filename= nom_thumbnail)
                    fich = File(open(nom_thumbnail,'rb'))
                    instance.thumbnail.save(name = instance.nom_fichier + '_thumb.jpeg', content = fich)
                    remove(nom_thumbnail)
                    
        elif type_fichier == 'application/pdf':

            with Image(filename=instance.fichier.path + '[0]') as img:
                with img.clone() as converted:
                    converted.format = 'jpeg'
                    converted.save(filename= nom_thumbnail)
                    fich = File(open(nom_thumbnail,'rb'))
                    instance.thumbnail.save(name = instance.nom_fichier + '_thumb.jpeg', content = fich)
                    remove(nom_thumbnail)

        else:
            pass
    else:
        pass