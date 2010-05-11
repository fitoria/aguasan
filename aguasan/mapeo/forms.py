from django.forms import ModelForm
from models import *

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto

class ProyectoMunicipioForm(ModelForm):
    class Meta:
        model = ProyectoMunicipio
        exclude = ['proyecto']

class ProyectoDonanteForm(ModelForm):
    class Meta:
        model = ProyectoDonante
        exclude = ['proyecto']

class ProyectoContraparteForm(ModelForm):
    class Meta:
        model = ProyectoContraparte
        exclude = ['proyecto']
