from django import forms
from django.conf import settings
from models import Donante, Contraparte, ProyectoDonante, ProyectoContraparte

class MontoField(forms.FloatField):
    '''FormField para el campo monto'''
    def clean(self, value):
        value = value.replace(settings.THOUSAND_SEPARATOR, '')
        try:
            return float(value)
        except:
            raise forms.ValidationError("Introduzca un numero")
        
def magic_queryset(model, id_proyecto):
    if model is Donante:
        lista_ids = list(ProyectoDonante.objects.filter(proyecto__id = id_proyecto).values('donante'))
        for i in range(len(lista_ids)):
            lista_ids[i] = lista_ids[i]['donante']
        return Donante.objects.filter(id__in = lista_ids)
    elif model is Contraparte:
        lista_ids = list(ProyectoContraparte.objects.filter(proyecto__id = id_proyecto).values('contraparte'))
        for i in range(len(lista_ids)):
            lista_ids[i] = lista_ids[i]['contraparte']
        return Contraparte.objects.filter(id__in = lista_ids)
    else:
        raise Exception('modelo no valido', model)
