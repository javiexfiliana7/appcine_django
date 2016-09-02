import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miproyecto.settings')

import django
django.setup()

from miapp_rango.models import Genero, Pelicula


def populate():

    genero1 = add_genero("Comedia")

    add_pelicula(genero=genero1,
        titulo="Di que si",
        url="http://www.filmaffinity.com/es/film418633.html")
    add_pelicula(genero=genero1,
        titulo="Como Dios",
        url="http://www.filmaffinity.com/es/film555335.html")
    add_pelicula(genero=genero1,
        titulo="Ace Ventura",
        url="http://www.filmaffinity.com/es/film557766.html")

    genero2 = add_genero("Fantastico")

    add_pelicula(genero=genero2,
        titulo="El hobbit",
        url="http://www.filmaffinity.com/es/film172611.html")
    add_pelicula(genero=genero2,
        titulo="El senor de los anillos",
        url="http://www.filmaffinity.com/es/film750283.html")
    add_pelicula(genero=genero2,
        titulo="Los vengadores",
        url="http://www.filmaffinity.com/es/film353018.html")


    # Print out what we have added to the user.
    for g in Genero.objects.all():
        for p in Pelicula.objects.filter(genero_pelicula=g):
            print "- {0} - {1}".format(str(g), str(p))

def add_pelicula(genero, titulo, url, visitas=0):
    peli = Pelicula.objects.get_or_create(genero_pelicula=genero, titulo=titulo)[0]
    peli.url=url
    peli.visitas=visitas
    peli.save()
    return peli

def add_genero(nombre_genero,votos=0):
    gene = Genero.objects.get_or_create(n_genero=nombre_genero)[0]
    gene.visitas_genero=votos
    gene.save()
    return gene

# Start execution here!
if __name__ == '__main__':
    print "Empieza el script de miapp_rango..."
    populate()
