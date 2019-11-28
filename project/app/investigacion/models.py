# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app.persona.models import Persona, File
from app.compania.models import Compania, Contacto, Sucursales
from app.agente.models import Labels

ACTIVO_OPCIONES = (
		(0, 'Sí/No'),
	    (1, 'Sí'),
	    (2, 'No'),
	)

class Investigacion(models.Model):
	TIPO_INVESTIGACION_OPCIONES = (		
		(1, 'Esc. Laboral'),
		(2, 'Esc. Socieconómico'),
		(3, 'Otro'),
	)
	RESULTADO_OPCIONES = (
		('0', 'Por evaluar'),
		('1', 'Viable'),
		('2', 'No viable'),
		('3', 'Con reservas'),
		('4', 'Cancelado'),
	)
	STATUS_OPCIONES = (
		('0', 'En Investigación'),
		('1', 'Pdt. por Cliente'),
		('2', 'Inv. Terminada'),
	)
	STATUS_GRAL_OPCIONES = (
		('0', 'Abierto'),
		('1', 'Pdt. por Cliente'),
		('2', 'Cerrada'),
	)
	
	agente = models.ForeignKey(User)
	candidato = models.ForeignKey(Persona)
	compania = models.ForeignKey(Compania)
	sucursal = models.ForeignKey(Sucursales, blank=True, null=True)
	contacto = models.ForeignKey(Contacto)
	fecha_recibido = models.DateField(blank=True, null=True)
	hora_recibido = models.CharField(max_length=30, blank=True, null=True)
	fecha_entrega = models.DateField(blank=True, null=True)
	puesto = models.CharField(max_length=140)

	observaciones = models.TextField(max_length=200, blank=True, null=True)
	entrevista = models.DateTimeField(blank=True, null=True)
	fecha_registro = models.DateField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	conclusiones = models.TextField(blank=True, null=True)
	resultado = models.CharField(max_length=30, choices=RESULTADO_OPCIONES, blank=True, null=True, default='0')
	archivo = models.ForeignKey(File, blank=True, null=True)
	folio = models.CharField(max_length=50, blank=True, null=True)
	presupuesto = models.CharField(max_length=50, blank=True, null=True)
	
	status = models.CharField(max_length=140, choices=STATUS_OPCIONES, null=True, blank=True, default='0') #En template: "Estatus de Inv. Laboral"
	status_active = models.BooleanField(default=True) # revisar si es necesario, si no borrarlo
	status_general = models.CharField(max_length=140, choices=STATUS_GRAL_OPCIONES, null=True, blank=True, default='0')
	observaciones_generales = models.TextField(max_length=200, blank=True, null=True)
	
	tipo_investigacion_status = models.IntegerField(max_length=140, choices=TIPO_INVESTIGACION_OPCIONES, null=True, blank=True)
	tipo_investigacion_texto = models.TextField(max_length=2000, blank=True, null=True)

	#Historia en empresa
	laboro_anteriormente = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)
	familiar_laborando = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)
	label = models.ForeignKey(Labels, blank=True, null=True)

	def __unicode__(self):
		return u'%s / %s' % (self.candidato, self.compania)
