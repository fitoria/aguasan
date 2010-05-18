 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from mapeo.models import *
from lugar.models import *
from django.utils import simplejson
from django.db import transaction
from lugar.models import Municipio
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.core import serializers
from django.template import RequestContext
from forms import *

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def formulario(request):
    if (request.method == 'POST'):
        form = ProyectoForm(request.POST)
        if form.is_valid():
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

def editar_proyecto(request,id):
    '''Editando proyecto en formulario por fuera'''
    p = Proyecto.objects.get(pk=id)
    if (request.method == 'POST'):
        form = ProyectoForm(request.POST,instance=p)
        if form.is_valid():
          proyecto = form.save()
          return redirect(proyecto)
        else:
            return render_to_response('mapeo/editar_proyecto.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        form = ProyectoForm(instance=p)
        return render_to_response('mapeo/editar_proyecto.html',
                                  {'form': form}, context_instance=RequestContext(request))


def proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    dicc = {'proyecto': proyecto}
    return render_to_response('mapeo/proyecto.html', dicc,
                              context_instance=RequestContext(request))
                              
def lista_proyecto_municipio(request,id):
    proyecto_mun = ProyectoMunicipio.objects.filter(municipio__id=id)
    proyecto_dept = ProyectoDepartamento.get(id=proyecto_num__proyecto__id)
    lista_proyecto = Proyecto.filter(id=proyecto_dept__proyecto__id)

def contrapartes_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoContraparteForm()
    dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_contraparte_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

def donantes_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoDonanteForm()
    dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_donante_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

def departamento_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoDepartamentoForm()
    dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_departamento_proyecto.html', dicc,
                                  context_instance=RequestContext(request))


def municipio_proyecto(request, id_proyecto, id_dept):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = ProyectoMunicipioForm()
    dicc = {'form': form, 'id_proyecto': id_proyecto,
            'id_dept': id_dept}
    return render_to_response('mapeo/agregar_municipio_proyecto.html', dicc,
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

def agregar_contraparte(request):
    '''Agregando contraparte en formulario por fuera'''
    form = ContraparteForm()
    if (request.method == 'POST'):
        form = ContraparteForm(request.POST)
        if form.is_valid():
          contraparte = form.save()
          return HttpResponseRedirect('/contrapartes/')
        else:
            return render_to_response('mapeo/agregar_contraparte.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        return render_to_response('mapeo/agregar_contraparte.html',
                                  {'form': form}, context_instance=RequestContext(request))

def agregar_donante(request):
    '''Agregando donante en formulario por fuera'''
    form = DonanteForm()
    if (request.method == 'POST'):
        form = DonanteForm(request.POST)
        if form.is_valid():
          donante = form.save()
          return HttpResponseRedirect('/donantes/')
        else:
            return render_to_response('mapeo/agregar_donante.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        return render_to_response('mapeo/agregar_donante.html',
                                  {'form': form}, context_instance=RequestContext(request))

def editar_donante(request,id):
    '''Editando donante en formulario por fuera'''
    d = Donante.objects.get(pk=id)
    if (request.method == 'POST'):
        form = DonanteForm(request.POST,instance=d)
        if form.is_valid():
          donante = form.save()
          return HttpResponseRedirect('/donantes/')
        else:
            return render_to_response('mapeo/editar_donante.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        form = DonanteForm(instance=d)
        return render_to_response('mapeo/editar_donante.html',
                                  {'form': form}, context_instance=RequestContext(request))

def editar_contraparte(request,id):
    '''Editando contraparte en formulario por fuera'''
    d = Contraparte.objects.get(pk=id)
    if (request.method == 'POST'):
        form = ContraparteForm(request.POST,instance=d)
        if form.is_valid():
          donante = form.save()
          return HttpResponseRedirect('/contrapartes/')
        else:
            return render_to_response('mapeo/editar_contraparte.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        form = ContraparteForm(instance=d)
        return render_to_response('mapeo/editar_contraparte.html',
                                  {'form': form}, context_instance=RequestContext(request))

def agregar_municipio_proyecto(request, id_proyecto, id_dept):
    '''se agrega municipio por medio de ajax'''
    #TODO: validar por id_dept
    if request.is_ajax():
        form = ProyectoMunicipioForm(request.POST)
        if form.is_valid():
            proyecto = ProyectoDepartamento.objects.get(proyecto=id_proyecto, departamento=id_dept)
            if proyecto:
                proyecto_municipio = form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                proyecto_municipio.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors), 
                                mimetype="application/json")
    else:
        return HttpResponse('ERROR')

def agregar_donante_proyecto(request, id):
    '''se agrega donante por medio de ajax'''
    if request.is_ajax():
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
            return HttpResponse(simplejson.dumps(form.errors),
                                mimetype="application/json")
    else:
        return HttpResponse('ERROR')

def agregar_contraparte_proyecto(request, id):
    '''se agrega contraparte por medio de ajax'''
    if request.is_ajax():
        form = ProyectoContraparteForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id)
            if proyecto:
                proyecto_contraparte = form.save(commit=False)
                proyecto_contraparte.proyecto = proyecto
                proyecto_contraparte.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors),
                                mimetype="application/json")
    else:
        return HttpResponse('ERROR')

def agregar_departamento_proyecto(request, id):
    ''' agrega departamento al proyecto por medio de ajax'''
    if request.is_ajax():
        form = ProyectoDepartamentoForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id)
            if proyecto:
                proyecto_departamento = form.save(commit=False)
                proyecto_departamento.proyecto = proyecto
                proyecto_departamento.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors), 
                                mimetype = 'application/json')
    else:
        return HttpResponse('ERROR')

def agregar_muincipio_proyecto(request, id_proyecto, id_dept):
    ''' agrega departamento al proyecto por medio de ajax'''
    if request.is_ajax():
        form = ProyectoDepartamentoForm(request.POST)
        if form.is_valid():
            proyecto = Proyecto.objects.get(id=id_proyecto)
            departamento = Departamento.objects.get(id=id)
            if proyecto and departamento:
                proyecto_municipio= form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                proyecto_municipio.departamento = departamento
                proyecto_municipio.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors), 
                                mimetype = 'application/json')
    else:
        return HttpResponse('ERROR')

def lista_donantes_proyecto(request, id):
    lista_donantes = ProyectoDonante.objects.filter(proyecto__id = id)
    resultados = []
    monto_total = 0
    for elemento in lista_donantes:
        dicc = {'id': elemento.id, 
                'donante': elemento.donante.nombre,
                'id_donante': elemento.donante.id,
                'id_proyecto': id,
                'monto': elemento.monto
                }
        monto_total += elemento.monto
        resultados.append(dicc)

    diccionario_resultado = {'lista': resultados, 'monto_total': monto_total} 
    return HttpResponse(simplejson.dumps(diccionario_resultado), 
            mimetype='application/json')

def lista_contrapartes_proyecto(request, id):
    lista_contrapartes = ProyectoContraparte.objects.filter(proyecto__id = id)
    resultados = []
    monto_total = 0
    for elemento in lista_contrapartes:
        dicc = {'id': elemento.id, 
                'contraparte': elemento.contraparte.nombre,
                'id_contraparte': elemento.contraparte.id,
                'id_proyecto': id,
                'monto': elemento.monto
                }
        monto_total += elemento.monto
        resultados.append(dicc)
    
    diccionario_resultado = {'lista': resultados, 'monto_total': monto_total} 
    return HttpResponse(simplejson.dumps(diccionario_resultado), 
            mimetype='application/json')

def mapa(request):
	return render_to_response('mapeo/mapa.html',context_instance=RequestContext(request))

def departamento(request,id):
    departamento=Departamento.objects.get(id=id)
    dicc = {'departamento': departamento}
    return render_to_response('mapeo/mapa_departamento.html', dicc,
                              context_instance=RequestContext(request))
