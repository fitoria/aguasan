from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('mapeo.views',
    (r'^index/$', 'index'),
    (r'^mapeo/formulario/$', 'formulario'),
    (r'^mapeo/mapa/$', 'mapa'),
    (r'^proyecto/(?P<id>\d+)/$', 'proyecto'),
    (r'^proyecto/(?P<id>\d+)/donantes/$', 'donantes_proyecto'),
    (r'^proyecto/(?P<id>\d+)/contrapartes/$', 'contrapartes_proyecto'),
    (r'^proyecto/(?P<id>\d+)/departamento/$', 'departamento_proyecto'),
    (r'^proyecto/(?P<id_proyecto>\d+)/departamento/(?P<id_dept>\d+)/municipio$', 'municipio_proyecto'),
    (r'^proyectos/$', 'lista_proyectos'),
    (r'^donantes/$', 'lista_donantes'),
    (r'^donantes/agregar/$', 'agregar_donante'),
    (r'^donantes/editar/(?P<id>\d+)/$', 'editar_donante'),
    (r'^contrapartes/$', 'lista_contrapartes'),
    (r'^contrapartes/agregar/$', 'agregar_contraparte'),
    (r'^contrapartes/editar/(?P<id>\d+)/$', 'editar_contraparte'),
    (r'^ajax/agregar/contraparte/(?P<id>\d+)/$', 'agregar_contraparte_proyecto'),
    (r'^ajax/agregar/donante/(?P<id>\d+)/$', 'agregar_donante_proyecto'),
    (r'^ajax/agregar/departamento/(?P<id>\d+)/$', 'agregar_departamento_proyecto'),
    (r'^ajax/agregar/municipio/(?P<id_proyecto>\d+)/(?P<id_dept>\d+)/$', 'agregar_municipio_proyecto'),
)
