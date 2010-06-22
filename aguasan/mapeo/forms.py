from django.forms import *
from models import *
from utils import *

class ProyectoForm(ModelForm):
    tipos = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(attrs={'class': ''}),
            queryset = TipoProyecto.objects.all(), )
    class Meta:
        model = Proyecto
        widgets = {
            'descripcion': Textarea(attrs={'class': 'textarea'}),
            'nombre': TextInput(attrs={'class': 'textbox_nombre'}),
            'website': TextInput(attrs={'class': 'textbox'}),
            'fecha_inicial': DateInput(attrs={'class': 'textbox'}, format="%d/%m/%Y"),
            'fecha_final': DateInput(attrs={'class': 'textbox'}, format="%d/%m/%Y"),
            'avance': Select(attrs={'class':'combobox'}),
        }

class ProyectoDepartamentoForm(ModelForm):
    class Meta:
        model = ProyectoDepartamento
        exclude = ['proyecto', 'monto_total']

class ProyectoMunicipioForm(ModelForm):
    
    donantes = None
    contrapartes = None
    def __init__(self, proyecto, *args, **kwargs):
        super(ProyectoMunicipioForm, self).__init__(*args, **kwargs)
        self.proyecto_id = proyecto.id
        self.donantes = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                queryset = magic_queryset(Donante, self.proyecto_id) , required=False)
        donantes = self.donantes
        self.contrapartes = ModelMultipleChoiceField(widget=CheckboxSelectMultiple, 
                queryset = magic_queryset(Contraparte, self.proyecto_id), required=False)
        contrapartes = self.contrapartes
        self.monto = MontoField()
    class Meta:
        model = ProyectoMunicipio
        exclude = ['proyecto']

class ProyectoDonanteForm(ModelForm):
    monto = MontoField()
    class Meta:
        model = ProyectoDonante
        exclude = ['proyecto']

class ProyectoContraparteForm(ModelForm):
    monto = MontoField()
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

class ProyectoFotosForm(ModelForm):
    class Meta:
        model = ProyectoFotos
        exclude = ['proyecto']
        widgets = {
            'fecha': TextInput(attrs={'class': 'textbox'}),
            }
