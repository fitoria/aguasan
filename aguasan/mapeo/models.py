# -*- coding: UTF-8 -*-
from django.db import models
from lugar.models import Municipio, Departamento
from django.utils.translation import ugettext as _
from thumbs import ImageWithThumbsField
from django.db.models import Sum

class Pais(models.Model):
    codigo = models.CharField(_("Codigo"), max_length=2, unique = True, 
                              help_text=_("Codigo pais mas info en: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"))
    nombre = models.CharField(max_length=100, unique = True)

    def __unicode__(self):
        return "%s(%s)" % (self.nombre, self.codigo)

    class Meta:
        verbose_name_plural = _('Paises')
        verbose_name = _('Pais')

class TipoDonante(models.Model):
    tipo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __unicode__(self):
        return self.tipo

class TipoContraparte(models.Model):
    tipo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __unicode__(self):
        return self.tipo

class Avance(models.Model):
    avance = models.CharField(max_length=100)

    def __unicode__(self):
        return self.avance

class TipoProyecto(models.Model):
    tipo = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.tipo

class Proyecto(models.Model):
    nombre = models.CharField(max_length=400)
    descripcion = models.TextField(_('Descripcion de medidas'))
    avance = models.ForeignKey(Avance)
    tipo = models.ForeignKey(TipoProyecto)
    fecha_inicial = models.DateField() 
    fecha_final = models.DateField() 
    logo = models.ImageField(upload_to='/proyecto/logos/', blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return "/proyecto/%d/" % self.id

class Donante(models.Model):
    nombre = models.CharField(max_length=150, unique = True)
    descripcion = models.TextField(_('Descripcion del donante'))
    logo = models.ImageField(upload_to='donante/logos/', blank=True)
    website = models.URLField(blank=True)
    pais = models.ForeignKey(Pais)
    tipo = models.ForeignKey(TipoDonante)

    def __unicode__(self):
        return self.nombre

class Contraparte(models.Model):
    nombre = models.CharField(max_length=150, unique = True)
    descripcion = models.TextField(_('Descripcion del donante'), blank=True)
    pais = models.ForeignKey(Pais)
    tipo = models.ForeignKey(TipoContraparte)
    logo = models.ImageField(upload_to='contraparte/logos/', blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.nombre

class ProyectoDepartamento(models.Model):
    '''Modelo usado para agregar todos los municipios y 
    guardar el monto total por departamento'''
    proyecto = models.ForeignKey(Proyecto)
    monto_total = models.FloatField(blank=True, default=0,  
                                   help_text=_('rellenar solo si no se dispone ' \
                                              'de informacion por municipio'))
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return"%s en %s" % (self.proyecto.nombre, self.departamento.nombre)
    
    def update_monto(self):
        '''Metodo para actualizar monto en caso de borrar o agregar cosas'''
        monto = ProyectoMunicipio.objects.filter(proyecto__id = self.id).aggregate(monto=Sum('monto'))
        self.monto_total = monto['monto']
        self.save()

    class Meta:
        unique_together = ['proyecto', 'departamento']

class ProyectoMunicipio(models.Model):
    municipio = models.ForeignKey(Municipio)
    monto = models.FloatField()
    donantes = models.ManyToManyField(Donante, null=True, blank=True) 
    contrapartes = models.ManyToManyField(Contraparte, null=True, blank=True) 
    proyecto = models.ForeignKey(ProyectoDepartamento)
    
    def __unicode__(self):
        return "%s - %s" % (self.municipio.nombre, self.proyecto.proyecto.nombre)

    def save(self, *args, **kwargs):
        super(ProyectoMunicipio, self).save(*args, **kwargs)
        self.proyecto.update_monto()

    def delete(self):
        super(ProyectoMunicipio, self).delete()
        self.proyecto.update_monto()

    class Meta:
        unique_together = ['proyecto', 'municipio']

class ProyectoDonante(models.Model):
    donante = models.ForeignKey(Donante)
    proyecto = models.ForeignKey(Proyecto)
    monto = models.FloatField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.donante.nombre, self.proyecto.nombre)

    class Meta:
        unique_together = ['proyecto', 'donante']

class ProyectoContraparte(models.Model):
    contraparte = models.ForeignKey(Contraparte)
    proyecto = models.ForeignKey(Proyecto)
    monto = models.FloatField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.contraparte.nombre, self.proyecto.nombre)

    class Meta:
        unique_together = ['proyecto', 'contraparte']

class ProyectoFotos(models.Model):
    '''Modelo para guardar las fotos de un proyecto'''
    proyecto = models.ForeignKey(Proyecto)
    #TODO: definir bien el tamano.
    foto = ImageWithThumbsField(upload_to='proyecto/fotos', sizes=((135, 115), (640,480),(800,600)))  
    titulo = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(auto_now=True)

    def __unicode__(self):
        return "%s (%s)" % (self.id, self.proyecto.nombre)

    class Meta:
        verbose_name_plural = 'Fotos del proyecto'
        verbose_name = 'Foto del proyecto'

