# -*- coding: utf-8 -*-
from django import forms

class FiltersForm(forms.Form):
	name = forms.CharField(label='Cliente', required=False)
	date_from = forms.CharField(label='Fecha Inicial', required=False)
	date_to = forms.CharField(label='Fecha Final', required=False)

	def __init__(self, *args, **kwargs):
		super(FiltersForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
