import os
from django.db import models
from django.utils.text import slugify


#def upload_to_projet(instance, filename):
    # Garder le nom de fichier original sans modification
#    return f'Images/{filename}'
import uuid
import os

def upload_to_projet(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'Images/{uuid.uuid4().hex}{ext}'



class ProjetBlog(models.Model):
    # Choix pour l'état du projet
    ETAT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('en_analyse', 'En analyse'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_projet, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_cours')
    langages = models.CharField(max_length=500, help_text="Entrez les langages séparés par des virgules (ex: Python, Django, HTML)", default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
