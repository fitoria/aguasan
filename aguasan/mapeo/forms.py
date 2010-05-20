from django.forms import ModelForm, Textarea, TextInput, Select
from models import *

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        widgets = {
            'descripcion': Textarea(attrs={'class': 'textarea'}),
            'nombre': TextInput(attrs={'class': 'textbox_nombre'}),
            'website': TextInput(attrs={'class': 'textbox'}),
            'fecha_inicial': TextInput(attrs={'class': 'textbox'}),
            'fecha_final': TextInput(attrs={'class': 'textbox'}),
            'avance': Select(attrs={'class':'combobox'}),
            'tipo': Select(attrs={'class':'combobox'}),
        }

class ProyectoDepartamentoForm(ModelForm):
    class Meta:
        model = ProyectoDepartamento
        exclude = ['proyecto', 'monto_total']

class ProyectoMunicipioForm(ModelForm):
    #def __init__(id_departamento):
        
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

class ContraparteForm(ModelForm):
    class Meta:
        model = Contraparte
        widgets = {
            'descripcion': Textarea(attrs={'class': 'textarea'}),
            'nombre': TextInput(attrs={'class': 'textbox_nombre'}),
            'website': TextInput(attrs={'class': 'textbox'}),
            'pais': Select(attrs={'class':'combobox'}),
            'tipo': Select(attrs={'class':'combobox'}),
        }

class DonanteForm(ModelForm):
    class Meta:
        model = Donante
        widgets = {
            'descripcion': Textarea(attrs={'class': 'textarea'}),
            'nombre': TextInput(attrs={'class': 'textbox_nombre'}),
            'website': TextInput(attrs={'class': 'textbox'}),
            'pais': Select(attrs={'class':'combobox'}),
            'tipo': Select(attrs={'class':'combobox'}),
        }
