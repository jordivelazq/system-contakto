# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from app.persona.models import *
from app.persona.forms import * 
from app.investigacion.models import *
from app.investigacion.forms import *
from app.compania.models import  *
from app.compania.forms import *
from app.entrevista.load_data import PreCandidato
from app.entrevista.forms import *
from app.entrevista.models import *
from app.entrevista.services import EntrevistaService
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from app.persona.services import PersonaService

from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from django.conf import settings
import datetime
import xlrd
import os
import json
from django.db.models import Q
from django.forms import ModelForm, Textarea


'''
	Entrevista (Excel)
'''
### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def editar_entrevista(request, investigacion_id, seccion_entrevista='datos-generales'):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')

	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	status_list = PersonaService.get_status_list(investigacion_id)
	page = 'candidatos'
	seccion = 'entrevista'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(pk=investigacion_id)
	candidato = investigacion.candidato
	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

	is_user_captura = request.user.groups.filter(name="captura").count()

	if not investigacion.entrevistapersona_set.all().count():
		if not seccion_entrevista == 'cita':
			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/cita')
		else:
			return render(request, 'sections/entrevista/blank_form.html', locals(), RequestContext(request))
	else:
		tiene_entrevista = True
		candidato = investigacion.entrevistapersona_set.all().order_by('-id')[0]

	data_seccion = {	'datos-generales'	: { 
					'titulo' 	: 'Datos Generales',
					'template' 	: 'sections/entrevista/forms/datos_grales_form.html' 
				},
				'info-personal'	: { 
					'titulo' 	: 'Información Personal',
					'template' 	: 'sections/entrevista/forms/info_personal_form.html' 
				},
				'salud'	: { 
					'titulo' 	: 'Salud, Actividades y Hábitos',
					'template' 	: 'sections/entrevista/forms/salud_form.html' 
				},
				'academica'	: { 
					'titulo' 	: 'Información Académica',
					'template' 	: 'sections/entrevista/forms/academica_form.html' 
				},
				'vivienda'	: { 
					'titulo' 	: 'Situación de la vivienda',
					'template' 	: 'sections/entrevista/forms/vivienda_form.html' 
				},
				'familia'	: { 
					'titulo' 	: 'Marco Familiar',
					'template' 	: 'sections/entrevista/forms/familia_form.html' 
				},
				'inf-economica'	: { 
					'titulo' 	: 'Información Económica',
					'template' 	: 'sections/entrevista/forms/sit_economica_form.html' 
				},
				'bienes'	: { 
					'titulo' 	: 'Bienes',
					'template' 	: 'sections/entrevista/forms/bienes_form.html' 
				},
				'referencias'	: { 
					'titulo' 	: 'Referencias Personales',
					'template' 	: 'sections/entrevista/forms/referencias_form.html' 
				},
				'evaluacion'	: {
					'titulo' 	: 'Evaluación',
					'template' 	: 'sections/entrevista/forms/evaluacion_form.html' 
				},
				'cita'	: { 
					'titulo' 	: 'Cita',
					'template' 	: 'sections/entrevista/forms/cita_form.html' 
				}

	}

	title = data_seccion[seccion_entrevista]['titulo']
	form_template = data_seccion[seccion_entrevista]['template']

	#DATOS GENERALES
	if seccion_entrevista == 'datos-generales':
		telefonos = EntrevistaTelefono.objects.filter(persona=candidato)
		direccion = EntrevistaDireccion.objects.get(persona=candidato)
		origen = EntrevistaOrigen.objects.get(persona=candidato)
		licencia = EntrevistaLicencia.objects.get(persona=candidato)

		TelefonoFormSet = modelformset_factory(EntrevistaTelefono, extra=0, exclude=('persona', 'categoria',))
		PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

		if request.method == 'POST' and not is_usuario_contacto:
			candidato_form = EntrevistaPersonaForm(request.POST, instance=candidato) # A form bound to the POST data
			tel_formset = TelefonoFormSet(request.POST, prefix='telefonos')
			direccion_form = EntrevistaDireccionForm(request.POST, instance=direccion)
			origen_form = EntrevistaOrigenForm(request.POST, instance=origen, prefix='origen')
			licencia_form = EntrevistaLicenciaForm(request.POST, instance=licencia)

			if candidato_form.is_valid() and tel_formset.is_valid() and direccion_form.is_valid() and origen_form.is_valid() and licencia_form.is_valid():
				candidato_form.save()
				tel_formset.save()
				direccion_form.save()
				origen_form.save()
				licencia_form.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			candidato_form = EntrevistaPersonaForm(instance=candidato)
			tel_formset = TelefonoFormSet(queryset=telefonos, prefix='telefonos')
			direccion_form = EntrevistaDireccionForm(instance=direccion)
			origen_form = EntrevistaOrigenForm(instance=origen, prefix='origen')
			licencia_form = EntrevistaLicenciaForm(instance=licencia)

	#INFO PERSONAL
	elif seccion_entrevista == 'info-personal':
		infopersonal = EntrevistaInfoPersonal.objects.get(persona=candidato)
		historial_empresa = EntrevistaHistorialEnEmpresa.objects.filter(persona=candidato)

		HistorialEmpresaFormset = modelformset_factory(EntrevistaHistorialEnEmpresa, extra=0, exclude=('persona', 'categoria',))

		if request.method == 'POST' and not is_usuario_contacto:
			infopersonal_form = EntrevistaInfoPersonalForm(request.POST, instance=infopersonal) # A form bound to the POST data
			historialempresa_formset = HistorialEmpresaFormset(request.POST, prefix='historial')
			if infopersonal_form.is_valid() and historialempresa_formset.is_valid():
				infopersonal_form.save()
				historialempresa_formset.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			infopersonal_form = EntrevistaInfoPersonalForm(instance=infopersonal)
			historialempresa_formset = HistorialEmpresaFormset(queryset=historial_empresa, prefix='historial')

	#SALUD, ACTIVIDADES Y HÁBITOS
	elif seccion_entrevista == 'salud':
		salud = EntrevistaSalud.objects.get(persona=candidato)
		actividades = EntrevistaActividadesHabitos.objects.get(persona=candidato)
	
		if request.method == 'POST' and not is_usuario_contacto:
			candidato_form = EntrevistaSaludPersonaForm(request.POST, instance=candidato) # A form bound to the POST data
			salud_form = EntrevistaSaludForm(request.POST, instance=salud, prefix='salud')
			actividades_form = EntrevistaActividadesHabitosForm(request.POST, instance=actividades, prefix='actividades')
			
			if candidato_form.is_valid() and salud_form.is_valid() and actividades_form.is_valid():
				candidato_form.save()
				salud_form.save()
				actividades_form.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			candidato_form = EntrevistaSaludPersonaForm(instance=candidato)
			salud_form = EntrevistaSaludForm(instance=salud, prefix='salud')
			actividades_form = EntrevistaActividadesHabitosForm(instance=actividades, prefix='actividades')

	#INFORMACIÓN ACADÉMICA
	elif seccion_entrevista == 'academica':
		academica = EntrevistaAcademica.objects.get(person=candidato)
		otro_idioma = EntrevistaOtroIdioma.objects.get(person=candidato)
		grados_escolares = EntrevistaGradoEscolaridad.objects.filter(person=candidato)

		GradoEscolaridadFormset = modelformset_factory(EntrevistaGradoEscolaridad, extra=0, exclude=('person', 'grado',))

		if request.method == 'POST' and not is_usuario_contacto:
			academica_form = EntrevistaAcademicaForm(request.POST, instance=academica)
			otro_idioma_form = EntrevistaOtroIdiomaForm(request.POST, instance=otro_idioma)
			gradosescolaridad_formset = GradoEscolaridadFormset(request.POST, prefix='grados')
			if academica_form.is_valid() and otro_idioma_form.is_valid() and gradosescolaridad_formset.is_valid():
				academica_form.save()
				otro_idioma_form.save()
				gradosescolaridad_formset.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			academica_form = EntrevistaAcademicaForm(instance=academica)
			otro_idioma_form = EntrevistaOtroIdiomaForm(instance=otro_idioma)
			gradosescolaridad_formset = GradoEscolaridadFormset(queryset=grados_escolares, prefix='grados')


	#SITUACIÓN VIVIENDA
	elif seccion_entrevista == 'vivienda':
		marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person=candidato, category=2)
		MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

		situacion_vivienda = EntrevistaSituacionVivienda.objects.get(person=candidato)
		propietario_vivienda = EntrevistaPropietarioVivienda.objects.get(person=candidato)
		caracteristicas_vivienda = EntrevistaCaractaristicasVivienda.objects.get(person=candidato)
		tipo_inmueble_vivienda = EntrevistaTipoInmueble.objects.get(person=candidato)
		distribucion_vivienda = EntrevistaDistribucionDimensiones.objects.get(person=candidato)

		if request.method == 'POST' and not is_usuario_contacto:
			situacion_vivienda_form = EntrevistaSituacionViviendaForm(request.POST, instance=situacion_vivienda)
			propietario_vivienda_form = EntrevistaPropietarioViviendaForm(request.POST, instance=propietario_vivienda)
			caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(request.POST, instance=caracteristicas_vivienda)
			tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(request.POST, instance=tipo_inmueble_vivienda)
			distribucion_vivienda = EntrevistaDistribucionDimensionesForm(request.POST, instance=distribucion_vivienda)
			marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados')

			if situacion_vivienda_form.is_valid() and propietario_vivienda_form.is_valid() and caracteristicas_vivienda_form.is_valid() and tipo_inmueble_vivienda_form.is_valid() and distribucion_vivienda.is_valid() and marcofamiliar_formset.is_valid():
				situacion_vivienda_form.save()
				propietario_vivienda_form.save()
				caracteristicas_vivienda_form.save()
				tipo_inmueble_vivienda_form.save()
				distribucion_vivienda.save()
				marcofamiliar_formset.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			situacion_vivienda_form = EntrevistaSituacionViviendaForm(instance=situacion_vivienda)
			propietario_vivienda_form = EntrevistaPropietarioViviendaForm(instance=propietario_vivienda)
			caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(instance=caracteristicas_vivienda)
			tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(instance=tipo_inmueble_vivienda)
			distribucion_vivienda = EntrevistaDistribucionDimensionesForm(instance=distribucion_vivienda)
			marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')
			
	#MARCO FAMILIAR
	elif seccion_entrevista == 'familia':
		marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person=candidato, category=1)
		MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

		if request.method == 'POST' and not is_usuario_contacto:
			marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados')
			if marcofamiliar_formset.is_valid():
				marcofamiliar_formset.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')
	
	#INFORMACIÓN ECONÓMICA
	elif seccion_entrevista == 'inf-economica':
		ingresos = EntrevistaEconomica.objects.filter(person=candidato, tipo='ingreso')
		egresos = EntrevistaEconomica.objects.filter(person=candidato, tipo='egreso')
		prestaciones_vivienda = EntrevistaPrestacionVivienda.objects.filter(persona=candidato)

		IngresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto'), form=MoneyFormatEntrevistaEconomicaForm)
		EgresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto',), form=MoneyFormatEntrevistaEconomicaForm)
		PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

		if request.method == 'POST' and not is_usuario_contacto:
			candidato.dependientes_economicos = request.POST.get('dependientes_economicos')
			ingresos_formset = IngresosFormset(request.POST, prefix='ingresos')
			egresos_formset = EgresosFormset(request.POST, prefix='egresos')
			pv_formset = PrestacionViviendaFormSet(request.POST, prefix='prestaciones')

			if ingresos_formset.is_valid() and egresos_formset.is_valid() and pv_formset.is_valid():
				candidato.save()
				ingresos_formset.save()
				egresos_formset.save()
				pv_formset.save()

				Bitacora(action='inf-economica: ' + str(investigacion_id), user=request.user).save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			candidato_form = EntrevistaPersonaInfoEconomicaForm(instance=candidato)
			ingresos_formset = IngresosFormset(queryset=ingresos, prefix='ingresos')
			egresos_formset = EgresosFormset(queryset=egresos, prefix='egresos')
			pv_formset = PrestacionViviendaFormSet(queryset=prestaciones_vivienda, prefix='prestaciones')
	
	#BIENES
	elif seccion_entrevista == 'bienes':
		tarjetas = EntrevistaTarjetaCreditoComercial.objects.filter(person=candidato)
		cuentas_deb = EntrevistaCuentaDebito.objects.filter(person=candidato)
		autos = EntrevistaAutomovil.objects.filter(person=candidato)
		bienesraices = EntrevistaBienesRaices.objects.filter(person=candidato)
		seguros = EntrevistaSeguro.objects.filter(person=candidato)
		deudas = EntrevistaDeudaActual.objects.filter(person=candidato)

		TarjetaCreditoComercialFormset = modelformset_factory(EntrevistaTarjetaCreditoComercial, extra=0, exclude=('person',), form=TarjetaCreditoComercialForm)
		CuentaDebitoFormset = modelformset_factory(EntrevistaCuentaDebito, extra=0, exclude=('person',), form=EntrevistaCuentaDebitoForm)
		AutomovilFormset = modelformset_factory(EntrevistaAutomovil, extra=0, exclude=('person',), form=EntrevistaAutomovilForm)
		BienesRaicesFormset = modelformset_factory(EntrevistaBienesRaices, extra=0, exclude=('person',), form=EntrevistaBienesRaicesForm)
		SeguroFormset = modelformset_factory(EntrevistaSeguro, extra=0, exclude=('person',))
		DeudaActualFormset = modelformset_factory(EntrevistaDeudaActual, extra=0, form=EntrevistaDeudaActualForm)

		if request.method == 'POST' and not is_usuario_contacto:
			tarjetas_formset = TarjetaCreditoComercialFormset(request.POST, prefix='tarjetas')
			cuentas_deb_formset = CuentaDebitoFormset(request.POST, prefix='cuentas_deb')
			autos_formset = AutomovilFormset(request.POST, prefix='autos')
			bienesraices_formset = BienesRaicesFormset(request.POST, prefix='bienesraices')
			seguros_formset = SeguroFormset(request.POST, prefix='seguros')
			deudas_formset = DeudaActualFormset(request.POST, prefix='deudas')

			if tarjetas_formset.is_valid() and cuentas_deb_formset.is_valid() and autos_formset.is_valid() and bienesraices_formset.is_valid() and seguros_formset.is_valid() and deudas_formset.is_valid():
				tarjetas_formset.save()
				cuentas_deb_formset.save()
				autos_formset.save()
				bienesraices_formset.save()
				seguros_formset.save()
				deudas_formset.save()

				Bitacora(action='bienes: ' + str(investigacion_id), user=request.user).save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			tarjetas_formset = TarjetaCreditoComercialFormset(queryset=tarjetas, prefix='tarjetas')
			cuentas_deb_formset = CuentaDebitoFormset(queryset=cuentas_deb, prefix='cuentas_deb')
			autos_formset = AutomovilFormset(queryset=autos, prefix='autos')
			bienesraices_formset = BienesRaicesFormset(queryset=bienesraices, prefix='bienesraices')
			seguros_formset = SeguroFormset(queryset=seguros, prefix='seguros')
			deudas_formset = DeudaActualFormset(queryset=deudas, prefix='deudas')

	#REFERENCIAS
	elif seccion_entrevista == 'referencias':
		referencias = EntrevistaReferencia.objects.filter(person=candidato)
		ReferenciaFormset = modelformset_factory(EntrevistaReferencia, extra=0, exclude=('person',), form=EntrevistaReferenciaForm)
		if request.method == 'POST' and not is_usuario_contacto:
			referencias_formset = ReferenciaFormset(request.POST, prefix='referencias')
			if referencias_formset.is_valid():
				referencias_formset.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			referencias_formset = ReferenciaFormset(queryset=referencias, prefix='referencias')

	#EVALUACIÓN
	elif seccion_entrevista == 'evaluacion':
		entrevista_investigacion = candidato.entrevistainvestigacion_set.all()[0]
		documentos = EntrevistaDocumentoCotejado.objects.filter(person=candidato)
		aspectos_hogar = EntrevistaAspectoHogar.objects.filter(person=candidato)
		aspectos_candidato = EntrevistaAspectoCandidato.objects.filter(person=candidato)

		DocumentoCotejadoFormset = modelformset_factory(EntrevistaDocumentoCotejado, extra=0, exclude=('person', 'tipo',), form=EntrevistaDocumentoCotejadoForm)
		AspectoHogarFormset = modelformset_factory(EntrevistaAspectoHogar, extra=0, exclude=('person', 'tipo',))
		AspectoCandidatoFormset = modelformset_factory(EntrevistaAspectoCandidato, extra=0, exclude=('person', 'tipo',))

		if request.method == 'POST' and not is_usuario_contacto:
			documentos_formset = DocumentoCotejadoFormset(request.POST, prefix='docs')
			aspectos_hogar_formset = AspectoHogarFormset(request.POST, prefix='asp_hogar')
			aspectos_candidato_formset = AspectoCandidatoFormset(request.POST, prefix='asp_candidato')
			investigacion_form = EntrevistaInvestigacionForm(request.POST, instance=entrevista_investigacion, prefix='investigacion')
			if documentos_formset.is_valid() and aspectos_hogar_formset.is_valid() and aspectos_candidato_formset.is_valid() and investigacion_form.is_valid():
				documentos_formset.save()
				aspectos_hogar_formset.save()
				aspectos_candidato_formset.save()
				investigacion_form.save()		

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			documentos_formset = DocumentoCotejadoFormset(queryset=documentos, prefix='docs')
			aspectos_hogar_formset = AspectoHogarFormset(queryset=aspectos_hogar, prefix='asp_hogar')
			aspectos_candidato_formset = AspectoCandidatoFormset(queryset=aspectos_candidato, prefix='asp_candidato')
			investigacion_form = EntrevistaInvestigacionForm(instance=entrevista_investigacion, prefix='investigacion')

	elif seccion_entrevista == 'cita':
		entrevista_cita = investigacion.entrevistacita_set.all().order_by('-id')[0]
		admin = 1 if request.user.is_superuser else 0

		if request.method == 'POST' and not is_usuario_contacto:
			cita_form = EntrevistaCitaForm(request.POST, instance=entrevista_cita)
			admin_form_flag = 1

			if cita_form.is_valid() and admin_form_flag:
				cita_form.save()		

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
		else:
			cita_form = EntrevistaCitaForm(instance=entrevista_cita)

	return render(request, 'sections/entrevista/edit_form.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
def cargar_entrevista(request, investigacion_id):
	if not request.user.is_staff and request.user.groups.filter(name="captura").count() == 0:
		return HttpResponseRedirect('/')

	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	status_list = PersonaService.get_status_list(investigacion_id)
	
	page = 'investigaciones'
	seccion = 'entrevista'
	seccion_entrevista = 'archivo'
	status = ''
	msg = ''
	tiene_entrevista = False

	investigacion = Investigacion.objects.get(id=investigacion_id)
	if investigacion.entrevistapersona_set.all().count():
		tiene_entrevista = True
		entrevista_actual = investigacion.entrevistapersona_set.all().order_by('-id')[0]
	
	if request.method == 'POST':

		if 'eliminar' in request.POST and tiene_entrevista:
			entrevista_actual.delete()
			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista')

		form = EntrevistaFileForm(request.POST, request.FILES)
		if form.is_valid():
			ext = os.path.splitext(str(request.FILES['record']))[1]
			pre_candidato = PreCandidato()
			if ext.lower() not in settings.EXT_RESEARCH_WHITELIST:
				pre_candidato.errors.append('Debes subir un archivo de Excel (xls o xlsx)')
			else:
				file_instance = EntrevistaFile(record=request.FILES['record'])
				file_instance.save()
				if (pre_candidato.leerArchivo(file_id=file_instance.id, sheet_index=0)):
					data = pre_candidato.getData()
					if 'nss' in data['candidato']['datos_generales'] and data['candidato']['datos_generales']['nss'] != investigacion.candidato.nss:
						pre_candidato.errors.append('NSS no coincide con el guardado en la investigación')

					#Revisar si hubo errores en la lectura del excel
					if len(pre_candidato.errors) == 0:
						candidato = ControllerPersona()
						candidato_id = candidato.saveAllData(investigacion, data, file_instance, request.user)
						#Revisar si hubo errores en la escritura de DB
						if len(candidato.errors) == 0:
							b = Bitacora(action='entrevista-cargada: ' + str(investigacion_id), user=request.user)
							b.save()
							if tiene_entrevista:
								entrevista_actual.delete()
							return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/exito')
						else:
							file_instance.delete()
							#borrar entrevista recién registrada si hubo algún error en la escritura de DB
							if candidato_id:
								EntrevistaPersona.objects.get(id=candidato_id).delete()
					else:
						file_instance.delete()

	else:
		form = EntrevistaFileForm()
	return render(request, 'sections/entrevista/new.html', locals(), RequestContext(request))

