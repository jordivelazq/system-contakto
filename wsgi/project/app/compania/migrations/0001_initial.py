# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Compania'
        db.create_table('compania_compania', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('telefono_alt', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=140, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('rfc_direccion', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('rfc', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('notas', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('es_cliente', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('razon_social', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('sucursal', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('referencia_correo', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('compania', ['Compania'])

        # Adding model 'Contacto'
        db.create_table('compania_contacto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compania', self.gf('django.db.models.fields.related.ForeignKey')(related_name='compania_contacto', to=orm['compania.Compania'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('puesto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=250)),
            ('email_alt', self.gf('django.db.models.fields.EmailField')(max_length=250, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('telefono_celular', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('telefono_otro', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('costo_inv_laboral', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('costo_inv_completa', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('compania', ['Contacto'])


    def backwards(self, orm):
        # Deleting model 'Compania'
        db.delete_table('compania_compania')

        # Deleting model 'Contacto'
        db.delete_table('compania_contacto')


    models = {
        'compania.compania': {
            'Meta': {'object_name': 'Compania'},
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'es_cliente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'notas': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'razon_social': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'referencia_correo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rfc_direccion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sucursal': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_alt': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'compania.contacto': {
            'Meta': {'object_name': 'Contacto'},
            'compania': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compania_contacto'", 'to': "orm['compania.Compania']"}),
            'costo_inv_completa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'costo_inv_laboral': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'email_alt': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_celular': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_otro': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['compania']