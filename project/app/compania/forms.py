# -*- coding: utf-8 -*-
from app.compania.models import *
from django import forms
from django.forms import ModelForm


class CompaniaAltaForm(ModelForm):
	class Meta:
		model = Compania
		fields = ['nombre',]

	def __init__(self, *args, **kwargs):
		super(CompaniaAltaForm, self).__init__(*args, **kwargs)
		# self.fields['nombre'].widget.attrs.update({'auto-complete': '', 'ui-items': 'names', 'ng-model':'selected', 'ng-change':'unset_compania_id()'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class CompaniaForm(ModelForm):
	class Meta:
		model = Compania
		exclude = ['fecha_creacion', 'status']

	def __init__(self, *args, **kwargs):
		super(CompaniaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if field_name is not 'es_cliente':
				field.widget.attrs['class'] = 'form-control'
				if 'telefono' in field_name and not field_name is "telefono_alt":
					field.widget.attrs['class'] = 'form-control phone'

class ContactoForm(ModelForm):
	class Meta:
		model = Contacto
		fields = ('nombre','email','email_alt','puesto','telefono','telefono_celular','telefono_otro','costo_inv_laboral','costo_inv_completa')

	def __init__(self, *args, **kwargs):
		super(ContactoForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			if 'telefono' == field_name or 'telefono_celular' == field_name:
				field.widget.attrs['class'] = 'form-control phone'
