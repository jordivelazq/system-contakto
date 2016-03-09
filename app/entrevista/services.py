from django.db import models
from django import forms

class EntrevistaService:

	@staticmethod
	def getDatosEntrevista(investigacion, entrevista = False):
		response = {}
		data = investigacion.entrevistacita_set.all()[0] if not entrevista else entrevista
		if data:
			response = {
				'entrevistador': data.entrevistador,
				'fecha': data.fecha_entrevista,
				'hora': data.hora_entrevista
			}
		return response

	@staticmethod
	def datefields_callback(field):
		if isinstance(field, models.DateField):
			return forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',])
		return field.formfield()

	@staticmethod
	def clean_telefono(s):
		try:
			return str(int(s))
		except ValueError:
			return str(s)