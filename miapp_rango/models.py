# TABLAS BASE DE DATOS

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Genero(models.Model):
    n_genero = models.CharField(max_length=128, unique=True)
    visitas_genero = models.IntegerField(default=0)
    slug_genero = models.SlugField()

    def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug_genero = slugify(self.n_genero)
                super(Genero, self).save(*args, **kwargs)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.n_genero

class Pelicula(models.Model):
    genero_pelicula = models.ForeignKey(Genero)#un genero puede contener muchas peliculas, una pelicula tiene un genero
    titulo  = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    portada = models.ImageField(upload_to='profile_images', blank=True)
    visitas = models.IntegerField(default=0)
    slug_pelicula = models.SlugField()

    def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug_pelicula = slugify(self.titulo)
                super(Pelicula, self).save(*args, **kwargs)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.titulo

class UserProfile(models.Model):
    user = models.OneToOneField(User) #asocia el UserProfile a el User

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
