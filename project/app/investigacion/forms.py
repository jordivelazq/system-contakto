# -*- coding: utf-8 -*-
from app.investigacion.models import *
from app.compania.models import Compania
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.db.models import Q
import time

'''
	Investigacion Form
'''
# forma para dar de alta candidato (investigacion)
class InvestigacionAltaForm(ModelForm):
	compania = forms.ModelChoiceField(queryset=Compania.objects.filter(es_cliente=True))
	agente = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com'))
	fecha_recibido = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',])
	
	class Meta:
		model = Investigacion
		exclude = ('candidato', 'conclusiones', 'resultado', 'archivo', 'folio', 'presupuesto','status_general','status','observaciones_generales')
		widgets = {
      'label': forms.HiddenInput()
    }

	def __init__(self, *args, **kwargs):
		super(InvestigacionAltaForm, self).__init__(*args, **kwargs)
		self.fields['fecha_recibido'].widget.attrs.update({'placeholder': 'dd/mm/yyyy', 'value': time.strftime("%d/%m/%Y")})
		self.fields['entrevista'].widget.attrs.update({'placeholder': 'dd/mm/yyyy HH:mm:ss'})
		self.fields['compania'].widget.attrs.update({'ng-model':'compania', 'ng-change': 'getContactsFromCompany()'})
		self.fields['observaciones'].widget.attrs.update({'rows':'2'})

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class InvestigacionEditarForm(ModelForm):
	compania = forms.ModelChoiceField(queryset=Compania.objects.filter(es_cliente=True))
	agente = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com'))
	fecha_recibido = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',])
	
	class Meta:
		model = Investigacion
		exclude = ('candidato', 'conclusiones', 'resultado', 'archivo', 'folio', 'presupuesto', 'status_general', 'status', 'observaciones_generales', 'tipo_investigacion_status', 'tipo_investigacion_texto', 'fecha_entrega')
		widgets = {
      'label': forms.HiddenInput(),
			'fecha_entrega': forms.HiddenInput()
    }

	def __init__(self, *args, **kwargs):
		self.agt_id = kwargs.pop('agt_id')
		super(InvestigacionEditarForm, self).__init__(*args, **kwargs)
		self.fields['fecha_recibido'].widget.attrs.update({'placeholder': 'dd/mm/yyyy', 'value': time.strftime("%d/%m/%Y")})
		self.fields['entrevista'].widget.attrs.update({'placeholder': 'dd/mm/yyyy HH:mm:ss'})
		self.fields['compania'].widget.attrs.update({'ng-model':'compania', 'ng-change': 'getContactsFromCompany()'})
		self.fields['observaciones'].widget.attrs.update({'rows':'2'})
		self.fields['agente'].queryset = User.objects.filter(Q(is_staff=True, is_active=True) | Q(is_staff=True,id=self.agt_id)).exclude(username='info@mintitmedia.com')

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class InvestigacionForm(ModelForm):
	compania = forms.ModelChoiceField(queryset=Compania.objects.filter(es_cliente=True))
	
	class Meta:
		model = Investigacion
		exclude = ('candidato', 'archivo', 'folio', 'presupuesto','status_general','status')

	def __init__(self, *args, **kwargs):
		super(InvestigacionForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class InvestigacionStatusForm(ModelForm):
	fecha_entrega = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',],required=False)
	
	class Meta:
		model = Investigacion
		fields = ('status', 'resultado', 'conclusiones', 'status_general', 'tipo_investigacion_status', 'tipo_investigacion_texto', 'fecha_entrega', 'label')

	def __init__(self, *args, **kwargs):
		super(InvestigacionStatusForm, self).__init__(*args, **kwargs)
		self.fields['conclusiones'].widget.attrs.update({'rows':'3'})
		self.fields['tipo_investigacion_texto'].widget.attrs.update({'rows':'3'})
		for field_name, field in self.fields.items():			
			field.widget.attrs['class'] = 'form-control'

class InvestigacionStatusTrayectoriaForm(ModelForm):	
	
	class Meta:
		model = Investigacion
		fields = ('observaciones_generales',)

	def __init__(self, *args, **kwargs):
		super(InvestigacionStatusTrayectoriaForm, self).__init__(*args, **kwargs)
		self.fields['observaciones_generales'].widget.attrs.update({'rows':'12'})
		for field_name, field in self.fields.items():			
			field.widget.attrs['class'] = 'form-control'

class InvestigacionGeneralForm(ModelForm):

	class Meta:
		model = Investigacion
		fields = ('status_general', 'observaciones_generales')

	def __init__(self, *args, **kwargs):
		super(InvestigacionGeneralForm, self).__init__(*args, **kwargs)

		self.fields['observaciones_generales'].widget.attrs.update({'rows':'3'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
