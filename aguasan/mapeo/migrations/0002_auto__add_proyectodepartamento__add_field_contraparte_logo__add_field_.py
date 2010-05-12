# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProyectoDepartamento'
        db.create_table('mapeo_proyectodepartamento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Proyecto'])),
            ('monto_total', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Departamento'])),
        ))
        db.send_create_signal('mapeo', ['ProyectoDepartamento'])

        # Adding field 'Contraparte.logo'
        db.add_column('mapeo_contraparte', 'logo', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True), keep_default=False)

        # Adding field 'Contraparte.website'
        db.add_column('mapeo_contraparte', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, blank=True), keep_default=False)

        # Adding field 'Proyecto.logo'
        db.add_column('mapeo_proyecto', 'logo', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True), keep_default=False)

        # Adding field 'Proyecto.website'
        db.add_column('mapeo_proyecto', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, blank=True), keep_default=False)

        # Adding field 'Donante.logo'
        db.add_column('mapeo_donante', 'logo', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True), keep_default=False)

        # Adding field 'Donante.website'
        db.add_column('mapeo_donante', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, blank=True), keep_default=False)

        # Deleting field 'ProyectoMunicipio.donante'
        db.delete_column('mapeo_proyectomunicipio', 'donante_id')

        # Adding M2M table for field donantes on 'ProyectoMunicipio'
        db.create_table('mapeo_proyectomunicipio_donantes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyectomunicipio', models.ForeignKey(orm['mapeo.proyectomunicipio'], null=False)),
            ('donante', models.ForeignKey(orm['mapeo.donante'], null=False))
        ))
        db.create_unique('mapeo_proyectomunicipio_donantes', ['proyectomunicipio_id', 'donante_id'])

        # Adding M2M table for field contrapartes on 'ProyectoMunicipio'
        db.create_table('mapeo_proyectomunicipio_contrapartes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyectomunicipio', models.ForeignKey(orm['mapeo.proyectomunicipio'], null=False)),
            ('contraparte', models.ForeignKey(orm['mapeo.contraparte'], null=False))
        ))
        db.create_unique('mapeo_proyectomunicipio_contrapartes', ['proyectomunicipio_id', 'contraparte_id'])

        # Changing field 'ProyectoMunicipio.proyecto'
        db.alter_column('mapeo_proyectomunicipio', 'proyecto_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.ProyectoDepartamento']))


    def backwards(self, orm):
        
        # Deleting model 'ProyectoDepartamento'
        db.delete_table('mapeo_proyectodepartamento')

        # Deleting field 'Contraparte.logo'
        db.delete_column('mapeo_contraparte', 'logo')

        # Deleting field 'Contraparte.website'
        db.delete_column('mapeo_contraparte', 'website')

        # Deleting field 'Proyecto.logo'
        db.delete_column('mapeo_proyecto', 'logo')

        # Deleting field 'Proyecto.website'
        db.delete_column('mapeo_proyecto', 'website')

        # Deleting field 'Donante.logo'
        db.delete_column('mapeo_donante', 'logo')

        # Deleting field 'Donante.website'
        db.delete_column('mapeo_donante', 'website')

        # Adding field 'ProyectoMunicipio.donante'
        db.add_column('mapeo_proyectomunicipio', 'donante', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['mapeo.Donante'], blank=True), keep_default=False)

        # Removing M2M table for field donantes on 'ProyectoMunicipio'
        db.delete_table('mapeo_proyectomunicipio_donantes')

        # Removing M2M table for field contrapartes on 'ProyectoMunicipio'
        db.delete_table('mapeo_proyectomunicipio_contrapartes')

        # Changing field 'ProyectoMunicipio.proyecto'
        db.alter_column('mapeo_proyectomunicipio', 'proyecto_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Proyecto']))


    models = {
        'lugar.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'lugar.municipio': {
            'Meta': {'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'mapeo.avance': {
            'Meta': {'object_name': 'Avance'},
            'avance': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mapeo.contraparte': {
            'Meta': {'object_name': 'Contraparte'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Pais']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoContraparte']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mapeo.donante': {
            'Meta': {'object_name': 'Donante'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Pais']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoDonante']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mapeo.pais': {
            'Meta': {'object_name': 'Pais'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'mapeo.proyecto': {
            'Meta': {'object_name': 'Proyecto'},
            'avance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Avance']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'fecha_final': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicial': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoProyecto']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mapeo.proyectocontraparte': {
            'Meta': {'object_name': 'ProyectoContraparte'},
            'contraparte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Contraparte']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectodepartamento': {
            'Meta': {'object_name': 'ProyectoDepartamento'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto_total': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectodonante': {
            'Meta': {'object_name': 'ProyectoDonante'},
            'donante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Donante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectomunicipio': {
            'Meta': {'object_name': 'ProyectoMunicipio'},
            'contrapartes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mapeo.Contraparte']", 'symmetrical': 'False'}),
            'donantes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mapeo.Donante']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.ProyectoDepartamento']"})
        },
        'mapeo.tipocontraparte': {
            'Meta': {'object_name': 'TipoContraparte'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'mapeo.tipodonante': {
            'Meta': {'object_name': 'TipoDonante'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'mapeo.tipoproyecto': {
            'Meta': {'object_name': 'TipoProyecto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mapeo']
