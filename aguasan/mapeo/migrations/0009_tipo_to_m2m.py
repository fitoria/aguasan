# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for proyecto in orm.Proyecto.objects.all():
            #por cada proyecto se migra!
            id_tipo = db.execute("select tipo_id from mapeo_proyecto where id=%s", 
                    [proyecto.id])[0][0]
            try:
                tipo = TipoProyecto.objects.get(id=id_tipo)
                proyecto.tipos.add(tipo)
                proyecto.save()
            except:
                print "tipo no encontrado, id: %s" % id_tipo

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")


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
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
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
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'tipos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mapeo.TipoProyecto']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mapeo.proyectocontraparte': {
            'Meta': {'unique_together': "(['proyecto', 'contraparte'],)", 'object_name': 'ProyectoContraparte'},
            'contraparte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Contraparte']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectodepartamento': {
            'Meta': {'unique_together': "(['proyecto', 'departamento'],)", 'object_name': 'ProyectoDepartamento'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto_total': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectodonante': {
            'Meta': {'unique_together': "(['proyecto', 'donante'],)", 'object_name': 'ProyectoDonante'},
            'donante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Donante']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"})
        },
        'mapeo.proyectofotos': {
            'Meta': {'object_name': 'ProyectoFotos'},
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'foto': ('mapeo.thumbs.ImageWithThumbsField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapeo.Proyecto']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'mapeo.proyectomunicipio': {
            'Meta': {'unique_together': "(['proyecto', 'municipio'],)", 'object_name': 'ProyectoMunicipio'},
            'contrapartes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mapeo.Contraparte']", 'null': 'True', 'blank': 'True'}),
            'donantes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mapeo.Donante']", 'null': 'True', 'blank': 'True'}),
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
