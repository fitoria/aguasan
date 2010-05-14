from django.forms import ModelForm, Textarea, TextInput
from models import *

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        widgets = {
            'descripcion': Textarea(attrs={'class': 'textarea'}),
            'nombre': TextInput(attrs={'class': 'textbox_nombre'}),
            'website': TextInput(attrs={'class': 'textbox'}),
            'fecha_inicial': TextInput(attrs={'class': 'textbox hasDatepicker'}),
            'fecha_final': TextInput(attrs={'class': 'textbox hasDatepicker'}),
            #TODO: ponerle bien la class a los combobox
        }

class ProyectoDepartamentoForm(ModelForm):
    class Meta:
        model = ProyectoDepartamento
        exclude = ['proyecto']

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

class ContraparteForm(ModelForm):
    class Meta:
        model = Contraparte

class DonanteForm(ModelForm):
    class Meta:
        model = Donante
