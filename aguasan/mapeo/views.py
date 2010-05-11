 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse
from mapeo.models import *
from django.utils import simplejson
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

def contrapartes_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoContraparteForm()
    dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_contrapartes.html', dicc,
                                  context_instance=RequestContext(request))
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    dicc = {'proyectos': proyectos}
    return render_to_response('mapeo/lista_proyectos.html', dicc,
                              context_instance=RequestContext(request))

def lista_donantes(request):
    donantes = Donante.objects.all()
    dicc = {'donantes': donantes}
    return render_to_response('mapeo/lista_donantes.html', dicc,
                              context_instance=RequestContext(request))

def lista_contrapartes(request):
    contrapartes = Contraparte.objects.all()
    dicc = {'contrapartes': contrapartes}
    return render_to_response('mapeo/lista_contrapartes.html', dicc,
                              context_instance=RequestContext(request))

def agregar_municipio_proyecto(request, id):
    '''se agrega municipio por medio de ajax'''
    if (request.method == 'POST'):
        form = ProyectoMunicipioForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id)
            if proyecto:
                proyecto_municipio = form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                proyecto_municipio.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors), mimetype="application/json")
    else:
        return HttpResponse('ERROR')

def agregar_donante_proyecto(request, id):
    '''se agrega donante por medio de ajax'''
    if (request.method == 'POST'):
        form = ProyectoDonanteForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id)
            if proyecto:
                proyecto_donante= form.save(commit=False)
                proyecto_donante.proyecto = proyecto
                proyecto_donante.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors), mimetype="application/json")
    else:
        return HttpResponse('ERROR')

def agregar_donante(request):
	return render_to_response('mapeo/agregar_donante.html',context_instance=RequestContext(request))

def agregar_contraparte(request):
	return render_to_response('mapeo/agregar_contraparte.html',context_instance=RequestContext(request))

def agregar_contraparte_proyecto(request, id):
    '''se agrega contraparte por medio de ajax'''
    print 'aljsdlajdsf'
    if request.is_ajax():
        form = ProyectoContraparteForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id)
            if proyecto:
                proyecto_contraparte = form.save(commit=False)
                proyecto_contraparte.proyecto = proyecto
                proyecto_contraparte.save()
                print 'se guardo'
                return HttpResponse('OK')
            else:
                print 'error'
                return HttpResponse('ERROR')
        else:
            print 'form no valido', form.errors
            return HttpResponse(simplejson.dumps(form.errors), mimetype="application/json")
    else:
        print 'request no es ajax'
        return HttpResponse('ERROR')

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

