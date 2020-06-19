# -*- coding: utf-8 -*-
from app.cobranza.models import Cobranza, Factura
from django import forms
from django.forms import ModelForm

class CobranzaMontoForm(ModelForm):
	class Meta:
		model = Cobranza
		fields = ['monto',]

	def __init__(self, *args, **kwargs):
		super(CobranzaMontoForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class FacturaForm(ModelForm):

	class Meta:
		model = Factura
		fields = ['folio', 'subtotal', 'total', 'fecha', 'rfc', 'nombre']

	def __init__(self, *args, **kwargs):
		super(FacturaForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class FacturaInvestigacionForm(ModelForm):

	class Meta:
		model = Factura
		fields = ['folio',]

	def __init__(self, *args, **kwargs):
		super(FacturaInvestigacionForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
