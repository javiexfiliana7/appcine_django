from django.conf.urls import patterns, url
from miapp_rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),#cuando no hay ninguna direccion
        url(r'^genero/(?P<genero_slug>[\w\-]+)/$', views.genero, name='genero'),
        url(r'^add_genero/$', views.add_genero, name='add_genero'),
        url(r'^genero/(?P<genero_slug>[\w\-]+)/add_pelicula/$', views.add_pelicula, name='add_pelicula'),
        url(r'^genero/(?P<genero_slug>[\w\-]+)/(?P<pelicula_slug>[\w\-]+)/$', views.pelicula, name='pelicula'),
        url(r'^registro/$', views.registro, name='registro'),
        url(r'^logueo/$', views.logueo, name='login'),
        url(r'^deslogueo/$', views.deslogueo, name='logout'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^eliminapeli/(?P<pelicula_slug>[\w\-]+)/$', views.eliminapeli, name='eliminapeli'),
        url(r'^genero/(?P<genero_slug>[\w\-]+)/(?P<pelicula_slug>[\w\-]+)/add_visitas/$', views.add_visitas, name='add_visitas'),
        url(r'^datos/$', views.reclama_datos, name="reclama_datos"),
        )
