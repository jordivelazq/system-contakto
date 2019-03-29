from django.db import models
from app.persona.models import Persona, File
from app.compania.models import Compania
import json

def has_info(data, prefix, investigacion):
	#Verifica los registros de la DB por modelo segun el 'prefix', si existe un registro del candidato, regresa TRUE
	if investigacion:
		if prefix=='prestacion_vivienda_infonavit' and  investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='infonavit').count():
			return True
		elif prefix=='prestacion_vivienda_fonacot' and  investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='fonacot').count():
			return True
		elif prefix=='origen' and  investigacion.candidato.origen_set.all().count():
			return True
		elif prefix=='direccion' and investigacion.candidato.direccion_set.all().count():
			return True
		elif prefix=='telefono1' and investigacion.candidato.telefono_set.filter(categoria='casa').count():
			return True
		elif prefix=='telefono2' and investigacion.candidato.telefono_set.filter(categoria='movil').count():
			return True
		elif prefix=='telefono3' and investigacion.candidato.telefono_set.filter(categoria='recado').count():
			return True
		elif prefix=='legalidad' and investigacion.candidato.legalidad_set.all().count():
			return True
		elif prefix=='seguro' and investigacion.candidato.seguro_set.all().count():
			return True

	#Verifica el contenido de los campos segun el 'prefix', si por lo menos 1 tiene info, regresa TRUE
	for field_name in data:
		if prefix in field_name:
			if data.get(field_name) != '':
				return True
	return False

def has_info_trayectoria(data, prefix, trayectoria):
	#Verifica los registros de la DB por modelo segun el 'prefix', si existe un registro del candidato, regresa TRUE
	if trayectoria:
		if prefix=='evaluacion' and trayectoria.evaluacion_set.all().count():
			return True
		elif prefix=='opinion_jefe' and trayectoria.evaluacion_set.all().count():
			if trayectoria.evaluacion_set.all()[0].opinion_set.filter(categoria='1').count():
				return True
		elif prefix=='opinion_rh' and trayectoria.evaluacion_set.all().count():
			if trayectoria.evaluacion_set.all()[0].opinion_set.filter(categoria='2').count():
				return True
		elif prefix=='informante1' and trayectoria.evaluacion_set.all().count():
			if trayectoria.evaluacion_set.all()[0].informante_set.all().count():
				return	True
		elif prefix=='informante2' and trayectoria.evaluacion_set.all().count():
			if trayectoria.evaluacion_set.all()[0].informante_set.all().count() > 1:
				return True

	#Verifica el contenido de los campos segun el 'prefix', si por lo menos 1 tiene info, regresa TRUE
	for field_name in data:
		if prefix in field_name:
			if data.get(field_name) != '':
				return True
	return False

def get_companias_json():
	response = []
	c = Compania.objects.all()
	for row in c:
		response.append({'label': row.nombre, 'id': row.id})
	return json.dumps(response)


