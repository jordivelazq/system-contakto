# -*- coding: utf-8 -*-
from app.cobranza.models import *
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