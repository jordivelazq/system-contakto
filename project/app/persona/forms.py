# -*- coding: utf-8 -*-
from app.persona.models import *
from django import forms
from django.forms import ModelForm

class FormaController():
	has_info = False
	is_valid = True

	def get_has_info(self):
		return self.has_info

	def get_is_valid(self):
		return self.is_valid

	def set_has_info(self, value):
		self.has_info = value

	def set_is_valid(self, value):
		self.is_valid = value

	"""docstring for FormasRegistroCandidato"""
	def __init__(self):
		super(FormasRegistroCandidato, self).__init__()

# formas para Alta
class CandidatoAltaForm(ModelForm):

	class Meta:  
		model = Persona
		fields = ['nombre', 'nss', 'rfc', 'email', 'edad', 'curp']

	def __init__(self, *args, **kwargs):
		super(CandidatoAltaForm, self).__init__(*args, **kwargs)
		self.fields['nss'].widget.attrs.update({'maxlength': '11'})
		self.fields['curp'].widget.attrs.update({'maxlength': '18'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			
			
			if field_name in ('nss', 'curp'):
				field.widget.attrs['ng-change'] = 'validate_candidate()'
				field.widget.attrs['ng-model'] = field_name

class TrayectoriaForm(ModelForm):
	'''
		Forma para: Investigacion Laboral > Empresa
	'''

	class Meta:  
		model = TrayectoriaLaboral
		exclude = ['agente', 'persona', 'status']

	def __init__(self, *args, **kwargs):
		super(TrayectoriaForm, self).__init__(*args, **kwargs)
		self.fields['funciones'].widget.attrs.update({'rows': '2'})
		self.fields['observaciones_generales'].widget.attrs.update({'rows': '2'})
		self.fields['cumplio_objetivos'].widget.attrs.update({'rows': '1'})
		self.fields['compania'].widget.attrs.update({'ng-model':'compania'})

		# se agrego clase 'money_format' a los campos que requieren este formato, pensando 
		# en usar JS para dar el formato
		fields_money_format = ['sueldo_inicial', 'sueldo_final']
		for field_name in fields_money_format:
			self.fields[field_name].widget.attrs['class'] = 'custom_money_format'

		for field_name, field in self.fields.items():
			if not field_name in ('terminada', 'visible_en_status'):
				field.widget.attrs['class'] = field.widget.attrs['class'] + ' form-control' if 'class' in field.widget.attrs else 'form-control'

class CartaLaboralForma(ModelForm, FormaController):

	class Meta:
		model = CartaLaboral
		fields = ['tiene_carta', 'expide', 'fecha']

	def __init__(self, *args, **kwargs):
		super(CartaLaboralForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class DatosGeneralesForma(ModelForm, FormaController):

	class Meta:
		model = DatosGenerales
		fields = ['num_personas', 'puestos', 'tiene_valores', 'motivo_salida', 'motivo_salida_candidato', 'tiene_sindicato', 'nombre_sindicato', 'es_recontratable', 'recontratable_motivo', 'tiene_mercancia', 'tiene_informacion', 'tiene_documentos', 'tiene_efectivo']

	def __init__(self, *args, **kwargs):
		super(DatosGeneralesForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if not field_name in ('tiene_mercancia', 'tiene_informacion', 'tiene_documentos', 'tiene_efectivo'):
				field.widget.attrs['class'] = 'form-control'

class TrayectoriaFormSoloCompania(ModelForm):

	class Meta:  
		model = TrayectoriaLaboral
		fields = ['compania',]

	def __init__(self, *args, **kwargs):
		super(TrayectoriaFormSoloCompania, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class EvaluacionForm(ModelForm):
	productividad = forms.ChoiceField(label='Productividad', widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	adaptabilidad = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	motivacion = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	puntualidad = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	asistencia = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	disponibilidad = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	responsabilidad = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	relacion_jefe_inmediato = forms.ChoiceField(label='Relación con jefe inmediato',widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	relacion_companeros = forms.ChoiceField(label='Relación con compañeros',widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	compromiso = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	honestidad = forms.ChoiceField(widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	toma_decisiones = forms.ChoiceField(label='Toma de decisiones', widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)
	solucion_problemas = forms.ChoiceField(label='Solución de problemas', widget=forms.RadioSelect(), choices=Evaluacion.EVALUACION_OPCIONES, required=False)

	class Meta:  
		model = Evaluacion
		exclude = ['trayectoriaLaboral']

	def __init__(self, *args, **kwargs):
		super(EvaluacionForm, self).__init__(*args, **kwargs)
		# for field_name, field in self.fields.items():
		# 	field.widget.attrs['class'] = 'form-control'

class InformanteForm(ModelForm):

	class Meta:  
		model = Informante
		exclude = ['evaluacion']

	def __init__(self, *args, **kwargs):
		super(InformanteForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class TelefonoForm(ModelForm, FormaController):

	class Meta:
		model = Telefono
		fields = ['numero', 'parentesco']

	def __init__(self, *args, **kwargs):
		super(TelefonoForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = ' form-control'
		
		self.fields['numero'].widget.attrs['class'] += ' phone'

class PrestacionViviendaForma(ModelForm, FormaController):

	class Meta:
		model = PrestacionVivienda
		fields = ['activo', 'numero_credito']

	def __init__(self, *args, **kwargs):
		super(PrestacionViviendaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class OrigenAltaForma(ModelForm, FormaController):
	fecha = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%d/%m/%Y',], required=False)

	class Meta:
		model = Origen
		fields = ['lugar', 'fecha', 'nacionalidad']

	def __init__(self, *args, **kwargs):
		super(OrigenAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class LegalidadAltaForma(ModelForm, FormaController):

	class Meta:
		model = Legalidad
		fields = ['sindicato', 'afiliado_sindicato']

	def __init__(self, *args, **kwargs):
		super(LegalidadAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class DemandaAltaForma(ModelForm, FormaController):

	class Meta:
		model = Demanda
		fields = ['tiene_demanda', 'empresa', 'motivo', 'ubicacion', 'fecha', 'audiencias', 'conclusion']
	
	def __init__(self, *args, **kwargs):
		super(DemandaAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class SeguroAltaForma(ModelForm, FormaController):

	class Meta:
		model = Seguro
		exclude = ['persona']

	def __init__(self, *args, **kwargs):
		super(SeguroAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class OpinionAltaForma(ModelForm):

	class Meta:
		model = Opinion
		fields = ['opinion', 'nombre', 'puesto', 'telefono', 'email']

	def __init__(self, *args, **kwargs):
		super(OpinionAltaForma, self).__init__(*args, **kwargs)
		self.fields['opinion'].widget.attrs.update({'rows': '3'})
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class InformanteAltaForma(ModelForm):

	class Meta:
		model = Informante
		exclude = ['evaluacion']

	def __init__(self, *args, **kwargs):
		super(InformanteAltaForma, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			


class CandidatoForm(ModelForm):

	class Meta:  
		model = Persona

	def __init__(self, *args, **kwargs):
		super(CandidatoForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class DireccionForm(ModelForm, FormaController):

	class Meta:
		exclude = ('persona',)
		model = Direccion

	def __init__(self, *args, **kwargs):
		super(DireccionForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class OrigenForm(ModelForm):
	
	class Meta:
		exclude = ('persona',)
		model = Origen

	def __init__(self, *args, **kwargs):
		super(OrigenForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class LicenciaForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = Licencia

	def __init__(self, *args, **kwargs):
		super(LicenciaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

'''
	Info Personal
'''
class InfoPersonalForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = InfoPersonal

	def __init__(self, *args, **kwargs):
		super(InfoPersonalForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

'''
	Salud
'''
class SaludForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = Salud

	def __init__(self, *args, **kwargs):
		super(SaludForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'
'''
	Actividades/Hábitos
'''
class ActividadesHabitosForm(ModelForm):
	class Meta:
		exclude = ('persona',)
		model = ActividadesHabitos

	def __init__(self, *args, **kwargs):
		super(ActividadesHabitosForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

'''
	Info Académica
'''
class AcademicaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = Academica

	def __init__(self, *args, **kwargs):
		super(AcademicaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class OtroIdiomaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = OtroIdioma

	def __init__(self, *args, **kwargs):
		super(OtroIdiomaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

'''
	Situación de la vivienda
'''
class SituacionViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = SituacionVivienda

	def __init__(self, *args, **kwargs):
		super(SituacionViviendaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class PropietarioViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = PropietarioVivienda

	def __init__(self, *args, **kwargs):
		super(PropietarioViviendaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class CaractaristicasViviendaForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = CaractaristicasVivienda

	def __init__(self, *args, **kwargs):
		super(CaractaristicasViviendaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class TipoInmuebleForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = TipoInmueble

	def __init__(self, *args, **kwargs):
		super(TipoInmuebleForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'

class DistribucionDimensionesForm(ModelForm):
	class Meta:
		exclude = ('person',)
		model = DistribucionDimensiones

	def __init__(self, *args, **kwargs):
		super(DistribucionDimensionesForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			#if not field_name in ('is_in_control', 'is_registered', 'client_authorization'):
			field.widget.attrs['class'] = 'form-control'



