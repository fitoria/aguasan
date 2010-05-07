from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('mapeo.views',
    (r'^index/$', 'index'),
    (r'^mapeo/formulario/$', 'formulario'),
    (r'^mapeo/mapa/$', 'mapa'),
    (r'^ajax/donantes_select$', 'donantes_select'),
    (r'^ajax/contrapartes_select$', 'contrapartes_select'),
    (r'^ajax/municipios_select/(?P<id_departamento>\d+)/$', 'municipios_select'),
)
