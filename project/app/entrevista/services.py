from os import path

from django.db import models
from django import forms
from app.adjuntos.models import Adjuntos

class EntrevistaService:

	@staticmethod
	def getDatosEntrevista(investigacion, entrevista = False):
		response = {}
		data = None
		if not entrevista and investigacion.entrevistacita_set.all().count() > 0:
			data = investigacion.entrevistacita_set.all()[0]
		elif entrevista:
			data = entrevista
		if data:
			response = {
				'entrevistador': data.entrevistador,
				'fecha': data.fecha_entrevista,
				'hora': data.hora_entrevista,
				'autorizada': data.autorizada
			}
		return response

	@staticmethod
	def datefields_callback(field):
		if isinstance(field, models.DateField):
			return forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',])
		return field.formfield()

	@staticmethod
	def clean_telefono(s):
		return s.encode('utf-8').strip()

def save_adjuntos(lista_adjuntos, image_path, absolute_path, investigacion):
	if not lista_adjuntos or not len(lista_adjuntos):
		return None

	nuevos_adjuntos, created = Adjuntos.objects.get_or_create(investigacion=investigacion)

	for field_name in lista_adjuntos:
		filename = lista_adjuntos[field_name]
		if filename and path.exists(absolute_path + '/' + filename):
			setattr(nuevos_adjuntos, field_name, image_path + '/' + filename)

	nuevos_adjuntos.save()
