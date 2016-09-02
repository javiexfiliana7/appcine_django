from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from miapp_rango.models import Genero, Pelicula
from miapp_rango.forms import UserForm, UserProfileForm, GeneroForm, PeliculaForm


#el request contiene informacion (metadatos) sobre la pagina para cargar la apropiada
#le pasamos una pregunta(request) y obtenemos una respuesta (response)
def some_view(request):
    if request.user.is_authenticated():
        return HttpResponse("estas logueado.")
    else:
        return HttpResponse("no estas logueado.")

#PAGINA PRINCIPAL
def index(request):
    lista_generos = Genero.objects.order_by('-visitas_genero')[:5]
    context_dict = {'generos': lista_generos} #diccionario con los generos que hemos obtenido en lista_generos
    return render(request, 'miapp_rango/index.html', context_dict)

#PAGINA DE CADA GENERO CON SUS PELICULAS
def genero(request, genero_slug):
    context_dict = {}
    #obtenemos todas las peliculas con ese genero
    try:
        genero = Genero.objects.get(slug_genero=genero_slug)
        genero.visitas_genero += 1;
        genero.save()
        context_dict['nombre_genero']=genero.n_genero
        context_dict['genero']=genero
        #obtenemos las peliculas con ese genero
        pelis=Pelicula.objects.filter(genero_pelicula=genero)
        context_dict['peliculas']=pelis
    except Genero.DoesNotExist:
        pass

    return render(request, 'miapp_rango/genero.html', context_dict)

def pelicula(request, genero_slug, pelicula_slug):
    context_dict = {}
    #obtenemos todas las peliculas con ese genero
    try:
        genero = Genero.objects.get(slug_genero=genero_slug)
        context_dict['nombre_genero']=genero.n_genero
        context_dict['genero']=genero
        #obtenemos las peliculas con ese genero
        pelicu=Pelicula.objects.get(slug_pelicula=pelicula_slug)
        context_dict['pelicula']=pelicu
    except Pelicula.DoesNotExist:
        pass

    return render(request, 'miapp_rango/pelicula.html', context_dict)

def eliminapeli(request, pelicula_slug):
    try:
        peli=Pelicula.objects.get(slug_pelicula=pelicula_slug)
        peli.delete()
        return HttpResponseRedirect('/miapp_rango/')
    except Pelicula.DoesNotExist:
        pass

def add_visitas(request, genero_slug, pelicula_slug):
    try:
        peli=Pelicula.objects.get(slug_pelicula=pelicula_slug)
        peli.visitas += 1;
        peli.save()
        return HttpResponseRedirect('/miapp_rango/genero/'+peli.genero_pelicula.slug_genero+'/'+peli.slug_pelicula+'/')
    except Pelicula.DoesNotExist:
        pass


#PAGINA PARA ANIADIR GENERO
def add_genero(request):

    if request.method == 'POST':
        form_genero = GeneroForm(request.POST)
        # comprobamos que es valido
        if form_genero.is_valid():
            form_genero.save(commit=True) # guardamos la category en la database.
            return index(request) # volvemos a la pagina principal
        else:
            # just print them to the terminal.
            print form_genero.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form_genero = GeneroForm()

    return render(request, 'miapp_rango/add_genero.html', {'form_genero': form_genero})


def add_pelicula(request, genero_slug):
    try:
        genero_peli = Genero.objects.get(slug_genero=genero_slug)#objeto
    except Genero.DoesNotExist:
                genero_peli = None

    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            if genero_peli:
                peli = form.save(commit=False)
                peli.genero_pelicula = genero_peli
                print '**************************************************************'
                if 'portada' in request.FILES:
                    print "hay imagen"
                    peli.portada = request.FILES['portada']
                peli.save()
                # probably better to use a redirect here.
                return HttpResponseRedirect('/miapp_rango/')
        else:
            print form.errors
    else:
        form = PeliculaForm()

    context_dict = {'form_pelicula':form, 'genero': genero_peli}

    return render(request, 'miapp_rango/add_pelicula.html', context_dict)

#LOGUEO
def logueo(request):
    if request.method == 'POST':
        # obtenemos los datos introducidos por el usuario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # usamos Django's para comprobar que el username/password
        # combinacion es valida - devuelve el usuario si lo cumple.
        usuario = authenticate(username=username, password=password)
        # si encuentra el usuario
        if usuario:
            # comprobamos que la cuenta esta activa
            if usuario.is_active:
                # si esta activa logueamos al usuario y redireccionamos a la pagina principal
                login(request,usuario) #el usuario va a estar conectado y queda senalado en el request
                return HttpResponseRedirect('/miapp_rango/') #en el request van los datos

            else:
                return HttpResponse("tu cuenta no esta activada.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "datos incorrectos: {0}, {1}".format(username, password)
            return HttpResponse("los datos introducidos son incorrectos.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'miapp_rango/login.html', {})

#DESLOGUEARSE
@login_required
def deslogueo(request):
    logout(request)
    return HttpResponseRedirect('/miapp_rango/')

#RESTRINGIDO
@login_required
def restricted(request):
    return HttpResponse("como estas logueado puedes ver este texto!")

#PAGINA DE REGISTRO
def registro(request):

    registered = False #true cuando se complete el registro

    if request.method == 'POST': #si viene con datos
        #recojemos los datos
        user_form = UserForm(data=request.POST) #rellenamos los formularios con los datos
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid(): #si los dos form son validos
            #----USER-----
            usuario = user_form.save()
            #obtenemos la contrasena y actualizamos el usuario
            usuario.set_password(usuario.password)
            usuario.save() #guardamos en la base de datos

            # ----PROFILE USER-----
            #como tenemos que asociar los datos el commit espera para guardar el modelo hasta que no haya problemas de integridad
            profile = profile_form.save(commit=False)
            profile.user = usuario #aqui los asociamos EL PROFILE TIENE UN USUARIO DENTRO

            #Comprobamos si hay una foto y actualizamos el perfil
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()  # guardamos UserProfile model instance.

            registered = True #registro completo

        # Invalid form or forms - mistakes or something else?
        else:
            print user_form.errors, profile_form.errors
    else: #si no es un http post, renderizamos usando dos instacias de ModelForm vacias,listas para meter datos
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    # Render the template depending on the context.
    return render(request,'miapp_rango/registro.html',context_dict)

#FUNCION QUE RECOJE LOS DATOS PARA LA GRAFICA
def reclama_datos(request):
    datos = ()#lista
    visitas = []
    lista_generos = []
    generos =  Genero.objects.order_by('-visitas_genero')
    for g in generos:
        lista_generos.append(g.n_genero)
        visitas.append(g.visitas_genero)

    datos = lista_generos, visitas
    return JsonResponse(datos, safe=False)#los envia al servidor
