 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from mapeo.models import *
from lugar.models import *
from django.utils import simplejson
from django.db import transaction
from lugar.models import Municipio
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.core import serializers
from django.core.validators import ValidationError
from django.template import RequestContext
from forms import *
from django.db.models import Sum


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
    monto_externo=ProyectoDonante.objects.filter(proyecto=id).aggregate(monto=Sum('monto'))['monto']
    monto_nacional=ProyectoContraparte.objects.filter(proyecto=id).aggregate(monto=Sum('monto'))['monto']
    if monto_externo and monto_nacional:
        monto_total_proyecto = monto_externo+monto_nacional
    elif monto_externo:
        monto_total_proyecto = monto_externo
    elif: monto_nacional: 
        monto_total_proyecto = monto_nacional
    else:
        monto_total_proyecto = 0

    dicc = {'proyecto': proyecto,'monto_externo':monto_externo,'monto_nacional':monto_nacional,'monto_total_proyecto':monto_total_proyecto}
    return render_to_response('mapeo/proyecto.html', dicc,
                              context_instance=RequestContext(request))

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
    if request.is_ajax():
        form = ProyectoMunicipioForm(request.POST)
        if form.is_valid():
            proyecto = ProyectoDepartamento.objects.get(proyecto=id_proyecto, departamento=id_dept)
            if proyecto:
                proyecto_municipio = form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                try:
                    proyecto_municipio.full_clean()
                    proyecto_municipio.save()
                except ValidationError, e:
                    error_dict = {'error': 'El municipio ya fue agregado'}
                    return HttpResponse(simplejson.dumps(error_dict),
                            mimetype='application/json')

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
                try:
                    proyecto_donante.full_clean()
                    proyecto_donante.save()
                except ValidationError, e:
                    error_dict = {'error': 'El cooperante ya fue agregado'}
                    return HttpResponse(simplejson.dumps(error_dict),
                            mimetype='application/json')

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
                try:
                    proyecto_contraparte.full_clean()
                    proyecto_contraparte.save()
                except ValidationError, e:
                    error_dict = {'error': 'La contraparte ya fue agregada'}
                    return HttpResponse(simplejson.dumps(error_dict),
                            mimetype='application/json')

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
                try:
                    proyecto_departamento.full_clean()
                    proyecto_departamento.save()
                except ValidationError, e:
                    error_dict = {'error': 'El departamento ya fue agregado'}
                    return HttpResponse(simplejson.dumps(error_dict),
                            mimetype='application/json')

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
            proyecto = ProyectoDepartamento.objects.get(id=id_proyecto, 
                    departamento__id=id_dept)
            if proyecto and departamento:
                proyecto_municipio= form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                try:
                    proyecto_municipio.full_clean()
                    proyecto_municipio.save()
                except ValidationError, e:
                    error_dict = {'error': 'El municipio ya fue agregado'}
                    return HttpResponse(simplejson.dumps(error_dict),
                            mimetype='application/json')

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

def lista_lugares(request, id):
    proyecto_departamentos = ProyectoDepartamento.objects.filter(proyecto__id = id)
    lista = []
    monto_total = 0
    for depart in proyecto_departamentos:
        proyecto_municipios = ProyectoMunicipio.objects.filter(proyecto = depart)
        lista_municipios = []
        for mun in proyecto_municipios:
            #TODO: agregarle contrapartes y esa shit
            dicc_municipios = {'municipio': mun.municipio.nombre,
                               'municipio_id': mun.municipio.id,
                               'monto': mun.monto,
                               }
            monto_total += mun.monto
            lista_municipios.append(dicc_municipios)

        dicc = {'departamento': depart.departamento.nombre,
                'municipios': lista_municipios,
                'id_proyecto': depart.proyecto.id,
                'id_departamento': depart.departamento.id,
                'monto_total': depart.monto_total,
                }
        lista.append(dicc)
        resultados = {'lista': lista, 'monto_total_proyecto': monto_total} 
    
    return HttpResponse(simplejson.dumps(resultados), 
            mimetype='application/json')
                
def mapa(request):
	return render_to_response('mapeo/mapa.html',context_instance=RequestContext(request))

def departamento(request,id):
    departamento=Departamento.objects.get(id=id)
    dicc = {'departamento': departamento}
    return render_to_response('mapeo/mapa_departamento.html', dicc,
                              context_instance=RequestContext(request))

def proyectos_municipio(request, id_municipio):
    '''listado de proyectos por municipio'''
    _proyectos_municipio = ProyectoMunicipio.objects.filter(municipio__id = id_municipio)
    proyectos = []
    for proyecto_municipio in _proyectos_municipio:
        proyectos.append(proyecto_municipio.proyecto.proyecto)

    return render_to_response('mapeo/proyectos_municipio.html', proyectos,
                              context_instance=RequestContext(request))

def proyectos_donante(request, id_donante):
    _proyectos_donante = ProyectoDonante.objects.filter(donante__id=id_donante)
    proyectos = []
    for proyecto_donante in _proyectos_donante:
        proyectos.append(proyecto_donante.proyecto)
    donante=Donante.objects.get(id=id_donante)
    return render_to_response('mapeo/proyectos_donante.html',{'donante':donante,'proyectos':proyectos},
                              context_instance=RequestContext(request))

def proyectos_departamento(request, id_dept):
    _proyectos_departamento = ProyectoDepartamento.objects.filter(departamento__id=id_dept)
    proyectos = []
    for proyecto_departamento in _proyectos_departamento:
        proyectos.append(proyecto_departamento)

    return render_to_response('mapeo/proyectos_departamento.html', proyectos,
                              context_instance=RequestContext(request))
