 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from mapeo.models import *
from django.contrib.auth.decorators import login_required
from lugar.models import *
from django.utils import simplejson
from django.db import transaction
from lugar.models import Municipio, Departamento
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.core import serializers
from django.core.validators import ValidationError
from django.template import RequestContext
from forms import *
from django.db.models import Sum


def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))
    
def ayuda(request):
    return render_to_response('ayuda.html',context_instance=RequestContext(request))

@login_required
def formulario(request):
    if (request.method == 'POST'):
        form = ProyectoForm(request.POST, request.FILES)
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

@login_required
def editar_proyecto(request,id):
    '''Editando proyecto en formulario por fuera'''
    p = Proyecto.objects.get(pk=id)
    if (request.method == 'POST'):
        form = ProyectoForm(request.POST, request.FILES, instance=p)
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
    elif monto_nacional: 
        monto_total_proyecto = monto_nacional
    else:
        monto_total_proyecto = 0

    dicc = {
            'proyecto': proyecto,
            'monto_externo':monto_externo,
            'monto_nacional':monto_nacional,
            'monto_total_proyecto':monto_total_proyecto
           }
    return render_to_response('mapeo/proyecto.html', dicc,
                              context_instance=RequestContext(request))
                                  
@login_required
def contrapartes_proyecto(request, id, action='crear'):
    if (action=='crear'):
        proyecto = get_object_or_404(Proyecto, id=id)
        form = ProyectoContraparteForm()
    else:
        proyecto_contraparte = ProyectoContraparte.objects.get(id=id)
        form = ProyectoContraparteForm(instance=proyecto_contraparte)

    dicc = {'form': form, 'id': id, 'action': action}
    return render_to_response('mapeo/agregar_contraparte_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

@login_required
def fotos_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoFotosForm()
    if (request.method == 'POST'):
        form = ProyectoFotosForm(request.POST, request.FILES)
        proyecto = get_object_or_404(Proyecto, id=id)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.proyecto = proyecto
            foto.save()
            dicc = {'form': form, 'id': id, 'guardado': True}
    else:
        dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_fotos_proyecto.html', dicc,
                              context_instance=RequestContext(request))

@login_required
def donantes_proyecto(request, id, action='crear'):
    if (action=='crear'):
        proyecto = get_object_or_404(Proyecto, id=id)
        form = ProyectoDonanteForm()
    else:
        proyecto_donante = get_object_or_404(ProyectoDonante, id=id)
        form = ProyectoDonanteForm(instance=proyecto_donante)
    
    dicc = {'form': form, 'id': id, 'action': action}
    return render_to_response('mapeo/agregar_donante_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

@login_required
def departamento_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    form = ProyectoDepartamentoForm()
    dicc = {'form': form, 'id': id}
    return render_to_response('mapeo/agregar_departamento_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    dicc = {'proyectos': proyectos}
    return render_to_response('mapeo/lista_proyectos.html', dicc,
                              context_instance=RequestContext(request))

def lista_donantes(request, template_name):
    donantes = Donante.objects.all().order_by('nombre')
    dicc = {'donantes': donantes}
    return render_to_response(template_name, dicc,
                              context_instance=RequestContext(request))

def lista_contrapartes(request, template_name):
    contrapartes = Contraparte.objects.all().order_by('nombre')
    dicc = {'contrapartes': contrapartes}
    return render_to_response(template_name, dicc,
                              context_instance=RequestContext(request))

@login_required
def agregar_contraparte(request):
    '''Agregando contraparte en formulario por fuera'''
    form = ContraparteForm()
    if (request.method == 'POST'):
        form = ContraparteForm(request.POST, request.FILES)
        if form.is_valid():
          contraparte = form.save()
          return HttpResponseRedirect('/contrapartes/')
        else:
            return render_to_response('mapeo/agregar_contraparte.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        return render_to_response('mapeo/agregar_contraparte.html',
                                  {'form': form}, context_instance=RequestContext(request))

@login_required
def agregar_donante(request):
    '''Agregando donante en formulario por fuera'''
    form = DonanteForm()
    if (request.method == 'POST'):
        form = DonanteForm(request.POST, request.FILES)
        if form.is_valid():
          donante = form.save()
          return HttpResponseRedirect('/donantes/')
        else:
            return render_to_response('mapeo/agregar_donante.html',
                                      {'form': form}, context_instance=RequestContext(request))
    else:
        return render_to_response('mapeo/agregar_donante.html',
                                  {'form': form}, context_instance=RequestContext(request))

@login_required
def editar_donante(request,id):
    '''Editando donante en formulario por fuera'''
    d = Donante.objects.get(pk=id)
    if (request.method == 'POST'):
        form = DonanteForm(request.POST, request.FILES, instance=d)
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

@login_required
def editar_contraparte(request,id):
    '''Editando contraparte en formulario por fuera'''
    d = Contraparte.objects.get(pk=id)
    if (request.method == 'POST'):
        form = ContraparteForm(request.POST, request.FILES, instance=d)
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

@login_required
def agregar_municipio_proyecto(request, id_proyecto, id_dept):
    '''se agrega municipio por medio de ajax'''
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    if (request.method=='POST'):
        form = ProyectoMunicipioForm(proyecto, request.POST)
        if form.is_valid():
            proyecto = ProyectoDepartamento.objects.get(proyecto=proyecto,
                                                        departamento=id_dept)
            if proyecto:
                proyecto_municipio = form.save(commit=False)
                proyecto_municipio.proyecto = proyecto
                try:
                    proyecto_municipio.full_clean()
                    proyecto_municipio.save()
                    form.save_m2m()
                    return render_to_response('mapeo/agregar_municipio_proyecto.html',
                                              {'form': form, 'cerrar': True, 
                                               'id_proyecto': id_proyecto, 'id_dept': id_dept}, 
                                              context_instance=RequestContext(request))
                except ValidationError, e:
                    return render_to_response('mapeo/agregar_municipio_proyecto.html',
                                               {'form': form, 'cerrar': False, 'error': 'El municipio ya fue agregado', 
                                               'id_proyecto': id_proyecto, 'id_dept': id_dept}, 
                                              context_instance=RequestContext(request))

            else:
                return render_to_response('mapeo/agregar_municipio_proyecto.html',
                                          {'form': form, 'cerrar': False, 
                                           'id_proyecto': id_proyecto, 'id_dept': id_dept}, 
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('mapeo/agregar_municipio_proyecto.html',
                                      {'form': form, 'cerrar': False, 
                                       'id_proyecto': id_proyecto, 'id_dept': id_dept}, 
                                      context_instance=RequestContext(request))
    else:
        form = ProyectoMunicipioForm(proyecto)
        form.fields['municipio'].queryset = Municipio.objects.filter(departamento__id=id_dept)
        dicc = {'form': form, 'id_proyecto': id_proyecto,
                'id_dept': id_dept}
        return render_to_response('mapeo/agregar_municipio_proyecto.html', dicc,
                                  context_instance=RequestContext(request))

@login_required
def editar_municipio_proyecto(request, id):
    proyecto_municipio = get_object_or_404(ProyectoMunicipio, id=id)
    if (request.method=='POST'):
        form = ProyectoMunicipioForm(proyecto_municipio.proyecto.proyecto, request.POST, instance=proyecto_municipio)
        if form.is_valid():
            if form.save():
                return render_to_response('mapeo/editar_municipio_proyecto.html',
                                              {'form': form, 'cerrar': True, 
                                               'id': id}, 
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('mapeo/editar_municipio_proyecto.html',
                                              {'form': form, 'cerrar': False, 
                                               'id': id}, 
                                              context_instance=RequestContext(request))
        else:
            return render_to_response('mapeo/editar_municipio_proyecto.html',
                                          {'form': form, 'cerrar': False, 
                                           'id': id}, 
                                          context_instance=RequestContext(request))
    else:
        form = ProyectoMunicipioForm(proyecto_municipio.proyecto.proyecto, instance=proyecto_municipio)
        form.contrapartes = proyecto_municipio.contrapartes
        form.donantes= proyecto_municipio.donantes
        return render_to_response('mapeo/editar_municipio_proyecto.html',
                                  {'form': form, 'cerrar': False, 
                                   'id': id}, 
                                  context_instance=RequestContext(request))
        
@login_required
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

@login_required
def editar_donante_proyecto(request, id):
    proyecto_donante = get_object_or_404(ProyectoDonante, id=id)
    if request.is_ajax():
        form = ProyectoDonanteForm(request.POST, instance=proyecto_donante)
        if form.is_valid():
            if form.save():
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors),
                                mimetype="application/json")
    else:
        return HttpResponse('ERROR')

@login_required
def editar_contraparte_proyecto(request, id):
    proyecto_contraparte= get_object_or_404(ProyectoContraparte, id=id)
    if request.is_ajax():
        form = ProyectoContraparteForm(request.POST, instance=proyecto_contraparte)
        if form.is_valid():
            if form.save():
                return HttpResponse('OK')
            else:
                return HttpResponse('ERROR')
        else:
            return HttpResponse(simplejson.dumps(form.errors),
                                mimetype="application/json")
    else:
        return HttpResponse('ERROR')

@login_required
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

@login_required
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

@login_required
def eliminar_elemento_proyecto(request, id, model):
    '''Metodo para eliminar elemento de un proyecto
    sirve para ProyectoContraparte, ProyectoMunicipio,
    ProyectoDepartamento, ProyectoDonante
    ejemplo de uso en el urls.py
    ('r^eliminar/foo/(?P<id>)/$', 'eliminar_elemento_proyecto', {'model': Foo}
    nota: tiene que ser vía ajax'''
    if request.is_ajax():
        elemento = get_object_or_404(model, id=id)
        elemento.delete()
        mensaje = '%s eliminado' % elemento.__unicode__()
        return HttpResponse(mensaje)
    else:
        raise Http404

@login_required
def eliminar_elemento(request, id, model, redirect_to):
    '''Metodo para eliminar un objeto y redirigir,
    ejemplo
    ('r^eliminar/foo/(?P<id>)/$', 'eliminar_elemento', {'model': Foo, 'redirect_to': '/bar/'}
    '''
    objeto = get_object_or_404(model, pk=id)
    objeto.delete()
    return HttpResponseRedirect(redirect_to)

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

    monto_total = '%.2f' % monto_total
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
    
    monto_total = '%.2f' % monto_total
    diccionario_resultado = {'lista': resultados, 'monto_total': monto_total} 
    return HttpResponse(simplejson.dumps(diccionario_resultado), 
            mimetype='application/json')

def lista_fotos_proyecto(request, id):
    lista_fotos = ProyectoFotos.objects.filter(proyecto__id=id)
    resultados = []
    for foto in lista_fotos:
        dicc = {
            'titulo': foto.titulo, 
            'descripcion': foto.descripcion,
            'thumbnail': foto.foto.url_135x115,
            'url_800x600': foto.foto.url_800x600,
            'url_640x480': foto.foto.url_640x480,
        }
        resultados.append(dicc)
    
    diccionario_resultado = {'lista': resultados}
    return HttpResponse(simplejson.dumps(diccionario_resultado),
                        mimetype='application/json')
        

def lista_lugares(request, id):
    proyecto_departamentos = ProyectoDepartamento.objects.filter(proyecto__id = id)
    lista = []
    monto_total = 0
    resultados = {'lista': [], 'monto_total_proyecto':0}
    for depart in proyecto_departamentos:
        proyecto_municipios = ProyectoMunicipio.objects.filter(proyecto = depart)
        lista_municipios = []
        for mun in proyecto_municipios:
            #TODO: agregarle contrapartes y esa shit
            dicc_municipios = {'municipio': mun.municipio.nombre,
                               'municipio_id': mun.municipio.id,
                               'monto': mun.monto,
                               'id': mun.id,
                               }
            monto_total += mun.monto
            lista_municipios.append(dicc_municipios)

        monto_total = '%.2f' % float(monto_total)
        dicc = {'departamento': depart.departamento.nombre,
                'municipios': lista_municipios,
                'id_proyecto': depart.proyecto.id,
                'id_departamento': depart.departamento.id,
                'monto_total': depart.monto_total,
                'id': depart.id,
                }
        lista.append(dicc)
        resultados = {'lista': lista, 'monto_total_proyecto': monto_total} 
    
    return HttpResponse(simplejson.dumps(resultados), 
            mimetype='application/json')

#Estas vistas tienen que ver con salidas#        
        
def mapa(request):
    proyectos = Proyecto.objects.all().count()
    cooperantes = Donante.objects.all().count()
    contrapartes = Contraparte.objects.all().count()
    monto_cooperante = ProyectoDonante.objects.all().aggregate(monto=Sum('monto'))['monto']
    monto_cooperante = float(monto_cooperante)
    monto_contraparte = ProyectoContraparte.objects.all().aggregate(monto=Sum('monto'))['monto']
    return render_to_response('mapeo/mapa.html',{'proyectos':proyectos,'contrapartes':contrapartes,'cooperantes':cooperantes,'monto_cooperante':monto_cooperante,'monto_contraparte':monto_contraparte},context_instance=RequestContext(request))

def departamento(request,id):
    departamento=Departamento.objects.get(id=id)
    _proyectos_dept = ProyectoDepartamento.objects.filter(departamento__id = id)
    proyectos = []
    for proyecto_departamento in _proyectos_dept:
        proyectos.append(proyecto_departamento.proyecto)
    num_proy = len(proyectos)
    if num_proy > 4:
        mas_proy="Ver Lista Completa"
    else:
        mas_proy=""
    dicc = {'departamento': departamento,'proyectos':proyectos[:4],'mas_proy':mas_proy,'num_proy':num_proy}
    return render_to_response('mapeo/mapa_departamento.html', dicc,
                              context_instance=RequestContext(request))

def proyectos_municipio(request, id_municipio):
    '''listado de proyectos por municipio'''
    _proyectos_municipio = ProyectoMunicipio.objects.filter(municipio__id = id_municipio)
    proyectos = []
    monto_total = 0
    for proyecto_municipio in _proyectos_municipio:
        proyectos.append(proyecto_municipio.proyecto.proyecto)
        monto_total += proyecto_municipio.proyecto.proyecto.monto_total()
    municipio=Municipio.objects.get(id=id_municipio)
    return render_to_response('mapeo/proyectos_municipio.html', 
                              {'proyectos':proyectos, 'monto_total': monto_total, 
                               'municipio':municipio},
                              context_instance=RequestContext(request))

def proyectos_departamento(request, id_departamento):
    '''listado de proyectos por departamento'''
    _proyectos_dept = ProyectoDepartamento.objects.filter(departamento__id = id_departamento)
    proyectos = []
    monto_total = 0
    for proyecto_departamento in _proyectos_dept:
        proyectos.append(proyecto_departamento.proyecto)
        monto_total+= proyecto_departamento.proyecto.monto_total()
    departamento=Departamento.objects.get(id=id_departamento)
    return render_to_response('mapeo/proyectos_departamento.html', 
                              {'proyectos':proyectos, 'monto_total': monto_total, 
                               'departamento':departamento},
                              context_instance=RequestContext(request))

def proyectos_donante(request, id_donante):
    _proyectos_donante = ProyectoDonante.objects.filter(donante__id=id_donante)
    proyectos = []
    monto_total = 0
    for proyecto_donante in _proyectos_donante:
        proyectos.append(proyecto_donante.proyecto)
        monto_total += proyecto_donante.proyecto.monto_total()
    donante=Donante.objects.get(id=id_donante)
    
    return render_to_response('mapeo/proyectos_donante.html', 
                              {'donante':donante,'proyectos':proyectos,
                               'monto_total': monto_total},
                              context_instance=RequestContext(request))
def proyectos_contraparte(request, id_contraparte):
    _proyectos_contraparte = ProyectoContraparte.objects.filter(contraparte__id=id_contraparte)
    proyectos = []
    monto_total = 0
    for proyecto_contraparte in _proyectos_contraparte:
        proyectos.append(proyecto_contraparte.proyecto)
        monto_total += proyecto_contraparte.proyecto.monto_total()

    contraparte = Contraparte.objects.get(id=id_contraparte)
    return render_to_response('mapeo/proyectos_contraparte.html',
                              {'contraparte':contraparte,'proyectos':proyectos, 
                               'monto_total': monto_total},
                              context_instance=RequestContext(request))

def proyectos_inversion(request, id_tipo):
    tipo = get_object_or_404(TipoProyecto, id=id_tipo)
    proyectos = Proyecto.objects.filter(tipo = tipo)
    dicc = {'proyectos': proyectos}
    return render_to_response('mapeo/proyectos_inversion.html', dicc,
                               context_instance=RequestContext(request))

def conteo_proyectos_municipio(request, id):
    '''devuelve un json con nombre del municipio
    y numero de proyectos'''
    #TODO: nombre de cooperantes en municipio 
    municipio = get_object_or_404(Municipio, id=id)
    proyectos = ProyectoMunicipio.objects.filter(municipio=municipio).all()
    donantes = []
    for proyecto in proyectos:
        donantes = donantes + list(proyecto.donantes.all())

    donantes = list(set(donantes))
    for i in range(len(donantes)):
        donantes[i] = {'donante': donantes[i].nombre, 
                       'url': donantes[i].get_absolute_url()}

    response = {'id': id, 'municipio': municipio.nombre, 
                'proyectos': proyectos.count(), 'donantes': donantes}

    return HttpResponse(simplejson.dumps(response),
                    mimetype='application/json')

def conteo_proyectos_departamento(request, id):
    '''devuelve un json con nombre del municipio
    y numero de proyectos'''
    departamento = get_object_or_404(Departamento, id=id)
    municipios = ProyectoMunicipio.objects.filter(proyecto__departamento = departamento)
    donantes = []
    for municipio in municipios:
        donantes = donantes + list(municipio.donantes.all())
    
    donantes = list(set(donantes))
    proyectos = ProyectoDepartamento.objects.filter(departamento=departamento).all().count()
    response = {'id': id, 'departamento': departamento.nombre, 
                'proyectos': proyectos, 'donantes': len(donantes)}
    return HttpResponse(simplejson.dumps(response),
                    mimetype='application/json')

def ubicacion_proyecto(request, model, id):
    '''Funcion para obtener la lista de lugares donde hay
    proyectos.
    model puede ser: Donante o Contraparte.'''
    resultados = [] #aca guardaremos las latitudes y longitudes.
    objeto = get_object_or_404(model, id=id)
    if "Donante" in str(model):
        proyectos_municipio = ProyectoMunicipio.objects.all().filter(donantes=objeto)
    elif "Contraparte" in str(model):
        proyectos_municipio = ProyectoMunicipio.objects.all().filter(contrapartes=objeto)
    else:
        raise Exception('model is not valid', str(model))
    

    for proyecto_municipio in proyectos_municipio:
        lat = float(proyecto_municipio.municipio.latitud)
        lon = float(proyecto_municipio.municipio.longitud)
        proyectos = Proyecto.objects.filter(proyectodepartamento__proyectomunicipio__municipio__id=proyecto_municipio.municipio.id).values('id', 'nombre')

        dicc = {'punto': (lon, lat), 
                'municipio': proyecto_municipio.municipio.nombre,
                'proyectos': list(proyectos) #hay que convertirlo a lista. A huevo
                }
        resultados.append(dicc)

    return HttpResponse(simplejson.dumps(resultados),
                        mimetype="application/json")
