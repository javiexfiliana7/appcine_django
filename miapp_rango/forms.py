from django import forms
from miapp_rango.models import Genero, Pelicula
from django.contrib.auth.models import User
from miapp_rango.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User #ponemos la clase y los campos que queremos que aparezcan
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile #el perfil creado en models.py
        fields = ('website', 'picture')


class GeneroForm(forms.ModelForm):
    n_genero = forms.CharField(max_length=128, help_text="Introduce el nombre del genero.")
    visitas_genero = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug_genero = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Asociacion entre el ModelForm y model
        model = Genero
        fields = ('n_genero',)


class PeliculaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=128, help_text="Introduce el titulo de la pelicula.")
    url = forms.URLField(max_length=200, help_text="URL de la peli.")
    visitas = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug_pelicula = forms.CharField(widget=forms.HiddenInput(), required=False)
    portada = forms.ImageField(required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Pelicula

        # no incluimos el campo
        exclude = ('genero_pelicula',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
