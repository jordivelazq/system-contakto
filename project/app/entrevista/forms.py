# -*- coding: utf-8 -*-
from app.entrevista.models import *
from django import forms
from django.forms import ModelForm, HiddenInput

class EntrevistaFileForm(ModelForm):

	class Meta:
		model = EntrevistaFile
		
	def __init__(self, *args, **kwargs):
		super(EntrevistaFileForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Datos generales
'''

class EntrevistaTelefonoForm(ModelForm):

	class Meta:
		model = EntrevistaTelefono
		exclude = ['persona', 'parentesco', 'categoria']

	def __init__(self, *args, **kwargs):
		super(EntrevistaTelefonoForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaPrestacionViviendaForma(ModelForm):
	
	class Meta:
		model = EntrevistaPrestacionVivienda
		fields = ['activo', 'numero_credito', 'fecha_tramite']

	def __init__(self, *args, **kwargs):
		super(EntrevistaPrestacionViviendaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaOrigenAltaForma(ModelForm):

	class Meta:
		model = EntrevistaOrigen
		fields = ['lugar', 'fecha']

	def __init__(self, *args, **kwargs):
		super(EntrevistaOrigenAltaForma, self).__init__(*args, **kwargs)
		self.fields['fecha'].widget.attrs.update({'placeholder': 'dd/mm/yyyy'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


class EntrevistaSeguroAltaForma(ModelForm):

	class Meta:
		model = EntrevistaSeguro
		exclude = ['persona']

	def __init__(self, *args, **kwargs):
		super(EntrevistaSeguroAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaDeudaActualForm(ModelForm):
	
	class Meta:
		model = EntrevistaDeudaActual
		exclude = ['person']

	def __init__(self, *args, **kwargs):
		super(EntrevistaDeudaActualForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			
class EntrevistaInvestigacionForm(ModelForm):

	class Meta:  
		model = EntrevistaInvestigacion
		fields = ('conclusiones', 'resultado')
		
	def __init__(self, *args, **kwargs):
		super(EntrevistaInvestigacionForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			if field_name == 'conclusiones':
				field.widget.attrs['class'] = 'form-control normal'
				field.widget.attrs.update({'rows':'20'})

class EntrevistaCitaForm(ModelForm):
	autorizada = forms.ChoiceField(choices=ACTIVO_OPCIONES, initial='0', label='Entrevista autorizada')
	entrevistador = forms.CharField(label='Enviado a entrevistador:', required=False)

	class Meta:  
		model = EntrevistaCita
		fields = ('entrevistador', 'fecha_entrevista', 'hora_entrevista', 'autorizada')

	def __init__(self, *args, **kwargs):
		super(EntrevistaCitaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaInvestigacionAdminForm(ModelForm):

	class Meta:
		model = EntrevistaInvestigacion
		fields = ('folio', 'presupuesto')

	def __init__(self, *args, **kwargs):
		super(EntrevistaInvestigacionAdminForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaPersonaForm(ModelForm):
	
	class Meta:  
		model = EntrevistaPersona
		exclude = ('investigacion', 'activa')

	def __init__(self, *args, **kwargs):
		super(EntrevistaPersonaForm, self).__init__(*args, **kwargs)
		self.fields['dependientes_economicos'].widget.attrs.update({'rows':'3'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaSaludPersonaForm(ModelForm):
	
	class Meta:  
		model = EntrevistaPersona
		fields = ('religion', 'religion_tiempo')

	def __init__(self, *args, **kwargs):
		super(EntrevistaSaludPersonaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaDireccionForm(ModelForm):

	class Meta:
		exclude = ('persona', 'investigacion')
		model = EntrevistaDireccion

	def __init__(self, *args, **kwargs):
		super(EntrevistaDireccionForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaOrigenForm(ModelForm):
	
	class Meta:
		exclude = ('persona',)
		model = EntrevistaOrigen

	def __init__(self, *args, **kwargs):
		super(EntrevistaOrigenForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaLicenciaForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = EntrevistaLicencia

	def __init__(self, *args, **kwargs):
		super(EntrevistaLicenciaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Info Personal
'''
class EntrevistaInfoPersonalForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = EntrevistaInfoPersonal

	def __init__(self, *args, **kwargs):
		super(EntrevistaInfoPersonalForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Salud
'''
class EntrevistaSaludForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = EntrevistaSalud

	def __init__(self, *args, **kwargs):
		super(EntrevistaSaludForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Actividades/Hábitos
'''
class EntrevistaActividadesHabitosForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = EntrevistaActividadesHabitos

	def __init__(self, *args, **kwargs):
		super(EntrevistaActividadesHabitosForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Info Académica
'''
class EntrevistaAcademicaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaAcademica

	def __init__(self, *args, **kwargs):
		super(EntrevistaAcademicaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaOtroIdiomaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaOtroIdioma

	def __init__(self, *args, **kwargs):
		super(EntrevistaOtroIdiomaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

'''
	Situación de la vivienda
'''
class EntrevistaSituacionViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaSituacionVivienda

	def __init__(self, *args, **kwargs):
		super(EntrevistaSituacionViviendaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaPropietarioViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaPropietarioVivienda

	def __init__(self, *args, **kwargs):
		super(EntrevistaPropietarioViviendaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaCaractaristicasViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaCaractaristicasVivienda

	def __init__(self, *args, **kwargs):
		super(EntrevistaCaractaristicasViviendaForm, self).__init__(*args, **kwargs)

		# se agrego clase 'money_format' a los campos que requieren este formato, pensando 
		# en usar JS para dar el formato
		fields_money_format = ['valor_aproximado', 'renta_mensual']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = field.widget.attrs['class'] + ' form-control' if 'class' in field.widget.attrs else 'form-control'

class EntrevistaTipoInmuebleForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaTipoInmueble

	def __init__(self, *args, **kwargs):
		super(EntrevistaTipoInmuebleForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaDistribucionDimensionesForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = EntrevistaDistribucionDimensiones

	def __init__(self, *args, **kwargs):
		super(EntrevistaDistribucionDimensionesForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EntrevistaObservacionesForm(ModelForm):
	class Meta:
		exclude = ('investigacion',)
		model = EntrevistaCita

	def __init__(self, *args, **kwargs):
		super(EntrevistaObservacionesForm, self).__init__(*args, **kwargs)

		self.fields['observaciones'].widget.attrs.update({'rows':'3'})
		for field_name, field in self.fields.items():			
			field.widget.attrs['class'] = 'form-control'

		self.fields['fecha_entrevista'].widget.attrs.update({'class':'form-control datepicker'})
		self.fields['hora_entrevista'].widget.attrs.update({'class':'form-control timepicker'})

'''
	Evaluacion
'''
class EntrevistaDocumentoCotejadoForm(ModelForm):

	class Meta:
		model = EntrevistaDocumentoCotejado

	def __init__(self, *args, **kwargs):
		super(EntrevistaDocumentoCotejadoForm, self).__init__(*args, **kwargs)
		self.fields['observaciones'].widget.attrs.update({'rows': '4'})
		self.fields['observaciones'].widget.attrs['class'] = 'form-control'

'''
	Referencia
'''
class EntrevistaReferenciaForm(ModelForm):

	class Meta:
		model = EntrevistaReferencia

	def __init__(self, *args, **kwargs):
		super(EntrevistaReferenciaForm, self).__init__(*args, **kwargs)
		self.fields['opinion'].widget.attrs.update({'rows': '4'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


class MoneyFormatEntrevistaEconomicaForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaEconomica

	def __init__(self, *args, **kwargs):
		super(MoneyFormatEntrevistaEconomicaForm, self).__init__(*args, **kwargs)

		fields_money_format = ['monto']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

class TarjetaCreditoComercialForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaTarjetaCreditoComercial

	def __init__(self, *args, **kwargs):
		super(TarjetaCreditoComercialForm, self).__init__(*args, **kwargs)
		
		fields_money_format = ['limite_credito', 'pago_minimo', 'saldo_actual']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

class EntrevistaCuentaDebitoForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaCuentaDebito

	def __init__(self, *args, **kwargs):
		super(EntrevistaCuentaDebitoForm, self).__init__(*args, **kwargs)
		
		fields_money_format = ['saldo_mensual', 'ahorro']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

class EntrevistaAutomovilForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaAutomovil

	def __init__(self, *args, **kwargs):
		super(EntrevistaAutomovilForm, self).__init__(*args, **kwargs)

		fields_money_format = ['valor_comercial']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

class EntrevistaBienesRaicesForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaBienesRaices

	def __init__(self, *args, **kwargs):
		super(EntrevistaBienesRaicesForm, self).__init__(*args, **kwargs)

		fields_money_format = ['valor_comercial']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

class EntrevistaDeudaActualForm(ModelForm):
	'''
	Helper class used to give money format to fields on Candidato > Entrevista  > Inf. Economica
	'''
	class Meta:
		model = EntrevistaDeudaActual
		widgets = {'person': HiddenInput()}

	def __init__(self, *args, **kwargs):
		super(EntrevistaDeudaActualForm, self).__init__(*args, **kwargs)

		fields_money_format = ['cantidad_total', 'saldo_actual', 'pago_mensual']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'



