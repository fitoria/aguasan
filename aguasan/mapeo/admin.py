from django.contrib import admin
from models import *

class AvanceAdmin(admin.ModelAdmin):
    pass

class TipoDonanteiAdmin(admin.ModelAdmin):
    pass

class TipoContraparteAdmin(admin.ModelAdmin):
    pass

class DonanteAdmin(admin.ModelAdmin):
    pass

class ContraparteAdmin(admin.ModelAdmin):
    pass

class PaisAdmin(admin.ModelAdmin):
    pass

class TipoProyectoAdmin(admin.ModelAdmin):
    pass

class ProyectoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(TipoProyecto, TipoProyectoAdmin)
admin.site.register(Avance, AvanceAdmin)
admin.site.register(TipoDonante, TipoDonanteiAdmin)
admin.site.register(TipoContraparte, TipoDonanteiAdmin)
admin.site.register(Donante, DonanteAdmin)
admin.site.register(Contraparte, ContraparteAdmin)
admin.site.register(Pais, PaisAdmin)
