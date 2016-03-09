# -*- coding: utf-8 -*-
from app.adjuntos.models import *
from django import forms
from django.forms import ModelForm

class AdjuntosForm(ModelForm):
	class Meta:
		model = Adjuntos
		exclude = ['investigacion',]


	def clean(self):

		doc_file_names = ('adj1',)
		doc_file_types = ('xlsx','xls','doc','docx','pdf')

		img_file_names = ('adj2','adj3','adj4','adj5','adj6','adj7','adj8','adj9','adj10','adj11','adj12','adj13')
		img_file_types = ('jpg','png','bmp','jpeg')

		for name in doc_file_names:
			f = self.cleaned_data[name]
			if f:
				ext = f.name.split('.')[len(f.name.split('.'))-1] if len(f.name.split('.')) > 1 else ''
				if ext.lower() not in doc_file_types:
					raise ValidationError('Error por extensión de archivos. Usar xlsx, xls, doc, docx, pdf para documentos y .jpg, .png, .bmp para imágenes')

		for name in img_file_names:
			f = self.cleaned_data[name]
			if f:
				ext = f.name.split('.')[len(f.name.split('.'))-1] if len(f.name.split('.')) > 1 else ''
				if ext.lower() not in img_file_types:
					raise ValidationError('Error por extensión de archivos. Usar xlsx, xls, doc, docx, pdf para documentos y .jpg, .png, .bmp para imágenes')

		return self.cleaned_data

	def __init__(self, *args, **kwargs):
		super(AdjuntosForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'