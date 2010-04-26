from django.db import models
from lugar.models import Municipio
from django.utils.translation import ugettext as _

class Pais(models.Model):
    codigo = models.CharField(_("Código"), max_length=2, unique = True, 
                              help_text=_("Código país mas info en: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"))
    nombre = models.CharField(max_length=100, unique = True)

    def __unicode__(self):
        return "%s(%s)" % (self.nombre, self.codigo)

class TipoDonante(models.Model):
    tipo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __unicode__(self):
        return self.tipo

class Proyecto(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(_('Descripción de medidas'))
    avance = models.CharField(_('Grado de avance'), max_length=100)

    def __unicode__(self):
        return self.nombre

class Donante (models.Model):
    nombre = models.CharField(max_length=150, unique = True)
    pais = models.ForeignKey(Pais)
    tipo = models.ForeignKey(TipoDonante)

    def __unicode__(self):
        return self.nombre

class ProyectoMunicipio(models.Model):
    municipio = models.ForeignKey(Municipio)
    monto = models.FloatField(min_value = 0)
    #se agregó donante por que puede ser que un municipio 
    #tenga un donante especifico
    donante = models.ForeignKey(Donante, blank=True, 
                                help_text=_("Puede dejar este campo en blanco si no se tiene información."))
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return "%s - %s" % (self.municipio.nombre, self.proyecto.nombre)

class ProyectoDonante(models.Model):
    donante = models.ForeignKey(Donante)
    proyecto = models.ForeignKey(Proyecto)
    monto = models.FloatField(min_value=0, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.donante.nombre, self.proyecto.nombre)
