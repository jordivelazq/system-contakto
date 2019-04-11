# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

ACTIVO_OPCIONES = (
		(0, 'Sí/No'),
	    (1, 'Sí'),
	    (2, 'No'),
	)

def validate_rfc(rfc):
	if rfc != '' and len(rfc) != 13:
		raise ValidationError('RFC debe tener 13 caracteres')

class Compania(models.Model):
	nombre = models.CharField(max_length=140, verbose_name='Nombre comercial')  #CHECK
	telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
	telefono_alt = models.CharField(max_length=20, verbose_name='Teléfono Alterno', blank=True, null=True)
	email = models.EmailField(max_length=140, verbose_name='Correo', blank=True, null=True) #CHECK
	role = models.CharField(max_length=140, verbose_name='Giro', blank=True, null=True) #CHECK
	rfc_direccion = models.CharField(max_length=250, verbose_name='Dirección Fiscal', blank=True, null=True) #CHECK
	rfc = models.CharField(max_length=20, verbose_name='RFC', blank=True, null=True, validators=[validate_rfc]) #CHECK
	notas = models.TextField(verbose_name='Notas', blank=True, null=True) #CHECK
	es_cliente = models.BooleanField(default=False, verbose_name='Es cliente') #CHECK
	razon_social = models.CharField(max_length=140, verbose_name='Razón social', blank=True, null=True)  #CHECK
	sucursal = models.CharField(max_length=140, verbose_name='Sucursal', blank=True, null=True)  #CHECK
	ciudad = models.CharField(max_length=140, verbose_name='Ciudad', blank=True, null=True)  #CHECK
	referencia_correo = models.IntegerField(default=0, verbose_name='Referencia por correo', choices=ACTIVO_OPCIONES, blank=True, null=True)

	fecha_creacion = models.DateField(auto_now=True)
	status = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.nombre)

	class Meta:
		verbose_name = 'Compañia'

class Contacto(models.Model):
	compania = models.ForeignKey(Compania, related_name='compania_contacto')

	nombre = models.CharField(max_length=140)
	puesto = models.CharField(max_length=140, blank=True, null=True)
	email = models.EmailField(max_length=250, verbose_name='Correo')
	email_alt = models.EmailField(max_length=250, verbose_name='Correo alterno', blank=True, null=True)
	telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
	telefono_celular = models.CharField(max_length=20, verbose_name='Teléfono celular', blank=True, null=True)
	telefono_otro = models.CharField(max_length=20, verbose_name='Otro', blank=True, null=True)
	
	costo_inv_laboral = models.FloatField(verbose_name='Costo de investigación laboral', blank=True, null=True)
	costo_inv_completa = models.FloatField(verbose_name='Costo de investigación completa', blank=True, null=True)
	
	status = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.nombre)

	class Meta:
		verbose_name = 'Contacto'
