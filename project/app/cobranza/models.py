# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app.investigacion.models import Investigacion

class Cobranza(models.Model):
	STATUS_OPCIONES_COBRANZA = (
	    ('0', 'Status 1'),
	    ('1', 'Status 2'),
	    ('2', 'Pagada'),
	)
	investigacion = models.ForeignKey(Investigacion)
	monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	# No. de factura
	folio = models.CharField(max_length=50, blank=True, null=True, default='')
	status_cobranza = models.CharField(max_length=140, choices=STATUS_OPCIONES_COBRANZA, null=True, blank=True, default='0')
	last_modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u'%s / %s' % (self.investigacion.candidato.nombre, self.investigacion.compania.nombre)

class Factura(models.Model):
	investigacion = models.ManyToManyField(Investigacion)

	folio = models.CharField(max_length=50, unique=True)
	subtotal = models.FloatField(default=0)
	total = models.FloatField(default=0)
	fecha = models.DateTimeField(blank=True, null=True)
