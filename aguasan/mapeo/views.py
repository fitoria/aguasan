 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse
from mapeo.models import *
from django.db import transaction
from lugar.models import Municipio
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from forms import *

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def formulario(request):
    if (request.method == 'POST'):
        form = ProyectoForm(request.POST)
        if form.is_valid():
           print form
           proyecto = form.save()
           request.session['mensaje'] = "El proyecto se a guardado correctamente, puede ahora editarlo"
           return redirect(proyecto)
        else:
            return render_to_response('mapeo/formulario.html', {'form': form},
                    context_instance=RequestContext(request))
    else:
        form = ProyectoForm()
        return render_to_response('mapeo/formulario.html', {'form': form},
                context_instance=RequestContext(request))

def proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    dicc = {'proyecto': proyecto}
    return render_to_response('mapeo/proyecto.html', dicc,
                              context_instance=RequestContext(request))

def agregar_municipio_proyecto(request, id):
    '''se agregaq municipio por medio de ajax'''
    if (request.method == 'POST'):
        form = ProyectoMunicipioForm(request.POST)
        if form.is_valid():
            print form
            proyecto_municipio = form.save()
        else:
            pass #retornar los errores en JSON
    else:
        pass #TODO: retornar error en JSON

def agregar_donante_proyecto(request, id):
    '''se agrega donante por medio de ajax'''
    if (request.method == 'POST'):
        form = ProyectoDonanteForm(request.POST)
        if form.is_valid():
            proyecto_donante = form.save()
        else:
            pass #retornar los errores en JSON
    else:
        pass #TODO: retornar error en JSON           
        
def mapa(request):
	return render_to_response('mapeo/mapa.html',context_instance=RequestContext(request))

def donantes_select(request):
    '''Vista para crear el select de donantes en el formulario'''
    donantes = Donante.objects.all()
    return render_to_response('mapeo/donantes_select.html', {'donantes': donantes})

def contrapartes_select(request):
    '''Vista para crear el select de contrapartes en el formulario'''
    contrapartes = Contraparte.objects.all()
    return render_to_response('mapeo/contrapartes_select.html', {'contrapartes': contrapartes})

def municipios_select(request, id_departamento):
    '''Vista para crear el select de municipio en el formulario'''
    municipios = get_list_or_404(Municipio, departamento__id = id_departamento)
    return render_to_response('mapeo/municipios_select.html', {'municipios': municipios, 'id': id_departamento})

