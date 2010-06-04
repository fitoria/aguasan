# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Municipio.latitud'
        db.alter_column('lugar_municipio', 'latitud', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=5, blank=True))

        # Changing field 'Municipio.longitud'
        db.alter_column('lugar_municipio', 'longitud', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=5, blank=True))


    def backwards(self, orm):
        
        # Changing field 'Municipio.latitud'
        db.alter_column('lugar_municipio', 'latitud', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=5, blank=True))

        # Changing field 'Municipio.longitud'
        db.alter_column('lugar_municipio', 'longitud', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=5, blank=True))


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
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['lugar']
