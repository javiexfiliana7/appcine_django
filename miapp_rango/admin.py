from django.contrib import admin
from miapp_rango.models import Genero, Pelicula, UserProfile


class GeneroAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_genero':('n_genero',)}

class PeliculaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_pelicula':('titulo',)}

# Register your models here.
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(UserProfile)
