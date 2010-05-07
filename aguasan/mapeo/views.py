 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse
from mapeo.models import *
from django.db import transaction
from lugar.models import Municipio
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

@transaction.commit_manually
def formulario(request):
    '''Fumado mode: ON'''
    if (request.method == 'POST'):
        #procesar esta shit abobinacion del demonio x_x
        proyecto = Proyecto()
        proyecto.nombre = request.POST['nombre']
        proyecto.descripcion = request.POST['descripcion']
        proyecto.fecha_inicial = request.POST['fecha_inicial']
        proyecto.fecha_final = request.POST['fecha_final']
        #TODO: Validar avance.
        proyecto.avance = request.POST['avance']

        
        
        #omg una transaccion.
        try:
            proyecto.save()
        except:
            transaction.rollback()
        else:
            transaction.commit()
    else:
        donantes = Donante.objects.all()
        contrapartes = Contraparte.objects.all()
        avances = Avance.objects.all()
        tipos_proyectos = TipoProyecto.objects.all()
        dicc = {'donantes': donantes, 'contrapartes': contrapartes, 
                'avances': avances, 'tipos_proyectos': tipos_proyectos}
        return render_to_response('mapeo/formulario.html', dicc, 
                                  context_instance=RequestContext(request))

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

