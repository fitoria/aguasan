# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Pais'
        db.create_table('mapeo_pais', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('mapeo', ['Pais'])

        # Adding model 'TipoDonante'
        db.create_table('mapeo_tipodonante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=30, db_index=True)),
        ))
        db.send_create_signal('mapeo', ['TipoDonante'])

        # Adding model 'TipoContraparte'
        db.create_table('mapeo_tipocontraparte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=30, db_index=True)),
        ))
        db.send_create_signal('mapeo', ['TipoContraparte'])

        # Adding model 'Avance'
        db.create_table('mapeo_avance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('avance', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mapeo', ['Avance'])

        # Adding model 'TipoProyecto'
        db.create_table('mapeo_tipoproyecto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mapeo', ['TipoProyecto'])

        # Adding model 'Proyecto'
        db.create_table('mapeo_proyecto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('avance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Avance'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.TipoProyecto'])),
            ('fecha_inicial', self.gf('django.db.models.fields.DateField')()),
            ('fecha_final', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('mapeo', ['Proyecto'])

        # Adding model 'Donante'
        db.create_table('mapeo_donante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Pais'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.TipoDonante'])),
        ))
        db.send_create_signal('mapeo', ['Donante'])

        # Adding model 'Contraparte'
        db.create_table('mapeo_contraparte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Pais'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.TipoContraparte'])),
        ))
        db.send_create_signal('mapeo', ['Contraparte'])

        # Adding model 'ProyectoMunicipio'
        db.create_table('mapeo_proyectomunicipio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Municipio'])),
            ('monto', self.gf('django.db.models.fields.FloatField')()),
            ('donante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Donante'], blank=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Proyecto'])),
        ))
        db.send_create_signal('mapeo', ['ProyectoMunicipio'])

        # Adding model 'ProyectoDonante'
        db.create_table('mapeo_proyectodonante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Donante'])),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Proyecto'])),
            ('monto', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('mapeo', ['ProyectoDonante'])

        # Adding model 'ProyectoContraparte'
        db.create_table('mapeo_proyectocontraparte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contraparte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Contraparte'])),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapeo.Proyecto'])),
            ('monto', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('mapeo', ['ProyectoContraparte'])


    def backwards(self, orm):
        
        # Deleting model 'Pais'
        db.delete_table('mapeo_pais')

        # Deleting model 'TipoDonante'
        db.delete_table('mapeo_tipodonante')

        # Deleting model 'TipoContraparte'
        db.delete_table('mapeo_tipocontraparte')

        # Deleting model 'Avance'
        db.delete_table('mapeo_avance')

        # Deleting model 'TipoProyecto'
        db.delete_table('mapeo_tipoproyecto')

        # Deleting model 'Proyecto'
        db.delete_table('mapeo_proyecto')

        # Deleting model 'Donante'
        db.delete_table('mapeo_donante')

        # Deleting model 'Contraparte'
        db.delete_table('mapeo_contraparte')

        # Deleting model 'ProyectoMunicipio'
        db.delete_table('mapeo_proyectomunicipio')

        # Deleting model 'ProyectoDonante'
        db.delete_table('mapeo_proyectodonante')

        # Deleting model 'ProyectoContraparte'
        db.delete_table('mapeo_proyectocontraparte')


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
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Pais']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoContraparte']"})
        },
        'mapeo.donante': {
            'Meta': {'object_name': 'Donante'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Pais']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoDonante']"})
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
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.TipoProyecto']"})
        },
        'mapeo.proyectocontraparte': {
            'Meta': {'object_name': 'ProyectoContraparte'},
            'contraparte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Contraparte']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
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
            'donante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Donante']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
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
