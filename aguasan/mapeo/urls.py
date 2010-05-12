from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('mapeo.views',
    (r'^index/$', 'index'),
    (r'^mapeo/formulario/$', 'formulario'),
    (r'^mapeo/mapa/$', 'mapa'),
    (r'^proyecto/(?P<id>\d+)/$', 'proyecto'),
    (r'^proyecto/(?P<id>\d+)/contrapartes/$', 'contrapartes_proyecto'),
    #(r'^proyecto/(<?P<id>\d+)/donantes/$', 'donantes'),
    (r'^proyectos/$', 'lista_proyectos'),
    (r'^donantes/$', 'lista_donantes'),
    (r'^contrapartes/$', 'lista_contrapartes'),
    (r'^contrapartes/agregar$', 'agregar_contraparte'),
    (r'^ajax/donantes_select$', 'donantes_select'),
    (r'^ajax/agregar/contraparte/(?P<id>\d+)/$', 'agregar_contraparte_proyecto'),
    (r'^ajax/agregar/donante/(?P<id>\d+)/$', 'agregar_donante_proyecto'),
    (r'^ajax/agregar/municipio/(?P<id>\d+)/$', 'agregar_municipio_proyecto'),
    (r'^ajax/donantes_select$', 'donantes_select'),
    (r'^ajax/contrapartes_select$', 'contrapartes_select'),
    (r'^ajax/municipios_select/(?P<id_departamento>\d+)/$', 'municipios_select'),
)
