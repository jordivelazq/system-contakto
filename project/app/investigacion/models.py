# -*- coding: utf-8 -*-

import datetime
from statistics import mode

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app.persona.models import Persona, File
from app.compania.models import Compania, Contacto, Sucursales
from app.agente.models import Labels, GestorInfo
from app.clientes.models import Cliente, ClienteSolicitud, ClienteSolicitudCandidato, ClienteUser
from app.core.models import Estado, Municipio

ACTIVO_OPCIONES = (
		(0, 'Sí/No'),
	    (1, 'Sí'),
	    (2, 'No'),
	)

def parse_string_to_date(string, fuzzy=False):
	if not string:
		return False

	try: 
		return datetime.datetime.strptime(string, "%d/%m/%Y")

	except ValueError:
		return False

class Investigacion(models.Model):
	TIPO_INVESTIGACION_OPCIONES = (		
		(1, 'Laboral'),
		(2, 'Socioeconómico'),
		(4, 'Psicometrías'),
		(5, 'Visita Domiciliaria'),
		(7, 'Visita Domiciliaria con demandas'),
		(6, 'Validación de Demandas'),
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
		('3', 'Abierto + Pdt. por Cliente'),
		('4', 'Cerrado + Pdt. por Cliente'),
	)
	
	agente = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	cliente_solicitud = models.ForeignKey(ClienteSolicitud, on_delete=models.CASCADE, blank=True, null=True)
	candidato = models.ForeignKey(Persona, on_delete=models.CASCADE)
	compania = models.ForeignKey(Compania, on_delete=models.CASCADE)
	sucursal = models.ForeignKey(Sucursales, models.SET_NULL, blank=True, null=True)
	contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, blank=True, null=True)
	fecha_recibido = models.DateField(blank=True, null=True) # Tenerla como fecha de asignacion del agente tomarla del sistema
	hora_recibido = models.CharField(max_length=30, blank=True, null=True)
	fecha_entrega = models.DateField(blank=True, null=True)
	puesto = models.CharField(max_length=140)

	# estado = models.ForeignKey(Estado, on_delete=models.CASCADE, blank=True, null=True)
	# municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)

	observaciones = models.TextField(max_length=200, blank=True, null=True)
	entrevista = models.DateTimeField(blank=True, null=True)
	fecha_registro = models.DateField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	conclusiones = models.TextField(max_length=16000, blank=True, null=True)
	resultado = models.CharField(max_length=30, choices=RESULTADO_OPCIONES, blank=True, null=True, default='0')
	archivo = models.ForeignKey(File, blank=True, null=True, on_delete=models.CASCADE)
	folio = models.CharField(max_length=50, blank=True, null=True)
	presupuesto = models.CharField(max_length=50, blank=True, null=True)
	
	status = models.CharField(max_length=140, choices=STATUS_OPCIONES, null=True, blank=True, default='0') #En template: "Estatus de Inv. Laboral"
	status_active = models.BooleanField(default=True) # revisar si es necesario, si no borrarlo
	status_general = models.CharField(max_length=140, choices=STATUS_GRAL_OPCIONES, null=True, blank=True, default='0')
	observaciones_generales = models.TextField(max_length=16000, blank=True, null=True)
	
	tipo_investigacion_status = models.IntegerField(choices=TIPO_INVESTIGACION_OPCIONES, null=True, blank=True)
	tipo_investigacion_texto = models.TextField(max_length=16000, blank=True, null=True)

	#Historia en empresa
	laboro_anteriormente = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)
	familiar_laborando = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)
	label = models.ForeignKey(Labels, blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return u'%s / %s' % (self.candidato, self.compania)
	
	def print_status_general(self):
		for status in self.STATUS_GRAL_OPCIONES:
			if status[0] == self.status_general:
				return status[1]

		return ""
	
	def get_trayectorias_laborales(self, use_status=None):
		trayectorias = self.candidato.trayectorialaboral_set.filter(status=True)
		if use_status:
			trayectorias = trayectorias.filter(visible_en_status=True)
		
		data = []
		for trayectoria in trayectorias:
			data.append(trayectoria)
		
		for i in range(len(data)):
			date_a = parse_string_to_date(data[i].periodo_alta)
			if not date_a:
				continue

			for j in range(len(data)):
				date_b = parse_string_to_date(data[j].periodo_alta)
				if not date_b:
					continue

				if date_a > date_b:
					tmp = data[i]
					data[i] = data[j]
					data[j] = tmp

		return data


class InvestigacionExtra(models.Model):
	investigacion = models.ForeignKey(Investigacion, on_delete=models.CASCADE)
	nombre = models.TextField(max_length=200, blank=True, null=True)
	apellido = models.TextField(max_length=200, blank=True, null=True)


class GestorInvestigacion(models.Model):
	ESTATUS = (
		(1, 'ASIGNADA'),
		(2, 'EN ATENCIÓN'),
		(3, 'CONCLUIDA')
	)
	investigacion = models.ForeignKey(Investigacion, on_delete=models.CASCADE)
	gestor = models.ForeignKey(GestorInfo, on_delete=models.CASCADE)
	fecha_asignacion = models.DateTimeField(null=True, blank=True)
	fecha_registro = models.DateTimeField(null=True, blank=True)
	fecha_atencion = models.DateTimeField(null=True, blank=True)
	estatus = models.PositiveSmallIntegerField(choices=ESTATUS, default=1)

	def __str__(self):
		return '{} / {} / {}'.format(self.investigacion,self.gestor, self.get_estatus_display())
