# -*- coding: utf-8 -*-
import pdb
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from app.persona.models import *
from app.persona.forms import * 
from app.investigacion.models import * 
from app.investigacion.forms import *
from app.investigacion.services import InvestigacionService
from app.compania.models import  *
from app.compania.forms import *
from app.entrevista.load_data import PreCandidato
from app.entrevista.forms import *
from app.entrevista.models import *
from app.entrevista.services import EntrevistaService
from app.cobranza.models import Cobranza, Factura
from app.cobranza.forms import CobranzaMontoForm, FacturaForm, GestorInvestigacionForm
from app.agente.models import Labels
from app.agente.forms import LabelsForm
from django.forms import modelformset_factory
from app.util.multiple_upload_investigacion import multiple_upload

from django.views.decorators.csrf import csrf_exempt

from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from app.persona.services import PersonaService, get_observacion_automatica
from app.entrevista.entrevista_persona import EntrevistaPersonaService

from django.conf import settings
import datetime
import xlrd
import os
import json
from django.db.models import Q

from reportlab.pdfgen import canvas

import logging

from app.adjuntos.models import Adjuntos
logger = logging.getLogger(__name__)

### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def panel(request):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	page = 'candidatos'	
	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	user_labels = Labels.objects.filter(agente = request.user)
	label_formset = modelformset_factory(Labels, form=LabelsForm, extra=0 if user_labels else len(Labels.LABEL_OPTIONS))

	is_user_captura = request.user.groups.filter(name="captura").count()

	messages = request.session.get('messages', [])
	request.session['messages'] = []
	
	if request.method == 'POST':
		if 'guardar' in request.POST:
			formset = label_formset(request.POST)
			if formset.is_valid():
				formset.save()
				return HttpResponseRedirect('/candidato/exito')
		
		if 'importar' in request.POST:
			form_file = EntrevistaFileForm(request.POST, request.FILES)
			if form_file.is_valid():
				ext = os.path.splitext(str(request.FILES['record']))[1]
				if ext.lower() not in settings.EXT_RESEARCH_WHITELIST:
					messages = [{
						"msg": "Es necesario cargar archivo de excel",
						"type": "danger"
					}]
				else:
					file_instance = EntrevistaFile(record=request.FILES['record'], tipo=1)
					file_instance.save()
					messages = multiple_upload(file_instance.id, 0, request.user)
					request.session['messages'] = messages

					return HttpResponseRedirect('/candidatos/exito')
	else:
		formset = label_formset(queryset=user_labels, initial=[{
				'color': color,
				'agente': request.user
			} for label, color in Labels.LABEL_OPTIONS])
		form_file = EntrevistaFileForm()

	return render(request, 'sections/candidato/panel.html', locals(), RequestContext(request))

'''
	Captura de nuevo candidato con info personal e investigación
'''
@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def crear(request):
	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)
	
	page = 'candidatos'
	status = ''
	msg = []
	companias_json = get_companias_json()
	DemandaFormSet = modelformset_factory(Demanda, form=DemandaAltaForma, max_num=1, extra=1)

	if request.method == 'POST':
		if 'cancelar' in request.POST:
			return HttpResponseRedirect('/candidatos')
		
		contact_id = request.POST.get('investigacion-contacto') or request.POST.get('contacto_id')

		formCandidato = CandidatoAltaForm(request.POST, prefix='candidato')
		formInvestigacion = InvestigacionAltaForm(request.POST, prefix='investigacion')
		formDireccion = DireccionForm(request.POST, prefix='direccion')
		formTelefono1 = TelefonoForm(request.POST, prefix='telefono1')
		formTelefono2 = TelefonoForm(request.POST, prefix='telefono2')
		formTelefono3 = TelefonoForm(request.POST, prefix='telefono3')
		formOrigen = OrigenAltaForma(request.POST, prefix='origen')
		formPrestacionViviendaInfonavit = PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit')
		formPrestacionViviendaFonacot = PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot')
		formLegalidad = LegalidadAltaForma(request.POST, prefix='legalidad')
		formDemanda = DemandaFormSet(request.POST, prefix='demanda')
		formSeguro = SeguroAltaForma(request.POST, prefix='seguro')

		if not formOrigen.is_valid():
			formOrigen.set_is_valid(False)

		if not formDireccion.is_valid():
			formDireccion.set_is_valid(False)

		if not formTelefono1.is_valid():
			formTelefono1.set_is_valid(False)

		if not formTelefono2.is_valid():
			formTelefono2.set_is_valid(False)

		if not formTelefono3.is_valid():
			formTelefono3.set_is_valid(False)

		if not formPrestacionViviendaInfonavit.is_valid():
			formPrestacionViviendaInfonavit.set_is_valid(False)

		if not formPrestacionViviendaFonacot.is_valid():
			formPrestacionViviendaFonacot.set_is_valid(False)

		if not formLegalidad.is_valid():
			formLegalidad.set_is_valid(False)

		if not formSeguro.is_valid():
			formSeguro.set_is_valid(False)

		if (formCandidato.is_valid()
			and formInvestigacion.is_valid()
			and formOrigen.get_is_valid()
			and formDireccion.get_is_valid()
			and formTelefono1.get_is_valid()
			and formTelefono2.get_is_valid()
			and formTelefono3.get_is_valid()
			and formPrestacionViviendaInfonavit.get_is_valid()
			and formPrestacionViviendaFonacot.get_is_valid()
			and formLegalidad.get_is_valid()
			and formSeguro.get_is_valid()
			and formDemanda.is_valid()):
			
			candidato = formCandidato.save()
			investigacion = formInvestigacion.save(commit=False)
			investigacion.candidato = candidato
			investigacion.status_active = True
			investigacion.status_general = '0'
			investigacion.save()

			#Registro en EntrevistaCita para datos de cita
			EntrevistaCita(investigacion=investigacion).save()

			origen = formOrigen.save(commit=False)
			origen.persona = investigacion.candidato
			origen.save()

			direccion = formDireccion.save(commit=False)
			direccion.persona = investigacion.candidato
			direccion.save()

			tel1 = formTelefono1.save(commit=False)
			tel1.persona = investigacion.candidato
			tel1.categoria = 'casa'
			tel1.save()

			tel2 = formTelefono2.save(commit=False)
			tel2.persona = investigacion.candidato
			tel2.categoria = 'movil'
			tel2.save()

			tel3 = formTelefono3.save(commit=False)
			tel3.persona = investigacion.candidato
			tel3.categoria = 'recado'
			tel3.save()

			infonavit = formPrestacionViviendaInfonavit.save(commit=False)
			infonavit.persona = investigacion.candidato
			infonavit.categoria_viv = 'infonavit'
			infonavit.save()

			fonacot = formPrestacionViviendaFonacot.save(commit=False)
			fonacot.persona = investigacion.candidato
			fonacot.categoria_viv = 'fonacot'
			fonacot.save()

			legalidad = formLegalidad.save(commit=False)
			legalidad.persona = investigacion.candidato
			legalidad.save()

			for formItem in formDemanda:
				demanda = formItem.save(commit=False)
				demanda.persona = investigacion.candidato
				demanda.save()

			seguro = formSeguro.save(commit=False)
			seguro.persona = investigacion.candidato
			seguro.save()

			### Crear registro cobranza:
			Cobranza(investigacion=investigacion).save()

			InvestigacionExtra(investigacion=investigacion, nombre=investigacion.agente.first_name, apellido=investigacion.agente.last_name).save()

			b = Bitacora(action='candidato-creado: ' + str(investigacion.candidato), user=request.user)
			b.save()

			#Se crea en Adjuntos
			Adjuntos(investigacion = investigacion).save()

			if 'guardar_crear_otro' in request.POST:
				return HttpResponseRedirect('/candidato/nuevo/exito')
			elif 'guardar_solo' in request.POST:
				return HttpResponseRedirect('/candidato/exito')
			elif 'guardar_empezar_inv' in request.POST:
				return HttpResponseRedirect('/candidato/investigacion/' + str(investigacion.id) + '/editar/exito')
			elif 'guardar_sucursal' in request.POST:
				return HttpResponseRedirect('/empresa/' + str(investigacion.compania.id) + '/sucursales?investigacion=' + str(investigacion.id))
			else:
				return HttpResponseRedirect('/candidato/exito')
		else:
			status = 'danger'
			msg.append('Favor de llenar los campos marcados con *')
			
	else:
		formCandidato = CandidatoAltaForm(prefix='candidato')
		initial_inv_data = '' if request.user.is_superuser else {'agente':request.user.id}
		formInvestigacion = InvestigacionAltaForm(prefix='investigacion', initial = initial_inv_data)
		formDireccion = DireccionForm(prefix='direccion')
		formTelefono1 = TelefonoForm(prefix='telefono1')
		formTelefono2 = TelefonoForm(prefix='telefono2')
		formTelefono3 = TelefonoForm(prefix='telefono3')
		formOrigen = OrigenAltaForma(prefix='origen')
		formPrestacionViviendaInfonavit = PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit')
		formPrestacionViviendaFonacot = PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot')
		formLegalidad = LegalidadAltaForma(prefix='legalidad')
		formDemanda = DemandaFormSet(queryset=Demanda.objects.none(), prefix='demanda')
		formSeguro = SeguroAltaForma(prefix='seguro')
		form_empresa = CompaniaQuickForm(prefix='empresa')
		form_empresa_contacto = ContactoQuickForm(prefix='empresa_contacto')
		
		
	return render(request, 'sections/candidato/crear.html', locals(), RequestContext(request))
	
### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def editar(request, investigacion_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')
	
	investigacion = Investigacion.objects.select_related('compania', 'candidato').get(id=investigacion_id)

	if not investigacion.status_active and not request.user.is_superuser:
		return HttpResponseRedirect('/')

	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	status_list = PersonaService.get_status_list(investigacion_id)

	page = 'candidatos'
	seccion = ''
	status = ''
	msg = []
	sucursales = investigacion.compania.sucursales_set.all()
	agente_id = investigacion.agente.id
	origen = investigacion.candidato.origen_set.all()
	direccion = investigacion.candidato.direccion_set.all()
	tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
	tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
	tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
	infonavit = investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='infonavit')
	fonacot = investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='fonacot')
	legalidad = investigacion.candidato.legalidad_set.all()
	demanda = investigacion.candidato.demanda_set.all()
	seguro = investigacion.candidato.seguro_set.all()
	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion) # NOTA: Pasar esto a PersonaService.get_status_list
	contact_id = investigacion.contacto.id

	is_user_captura = request.user.groups.filter(name="captura").count()
	DemandaFormSet = modelformset_factory(Demanda, form=DemandaAltaForma, max_num=1, extra=1)
	view = 'edit'

	if request.method == 'POST' and not is_usuario_contacto:
		msg_param = '/exito'

		if 'cancelar' in request.POST:
			return HttpResponseRedirect('/candidatos')

		formCandidato = CandidatoAltaForm(request.POST, prefix='candidato', instance=investigacion.candidato)
		if formCandidato.is_valid():
			formCandidato.save()
		else:
			msg_param = ''

		####################### Origen #######################
		formOrigen = OrigenAltaForma(request.POST, prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(request.POST, prefix='origen')
		if has_info(request.POST, prefix='origen', investigacion=investigacion):
			if formOrigen.is_valid():
				origen = formOrigen.save(commit=False)
				origen.persona = investigacion.candidato
				origen.save()
			else:
				msg_param = ''
		####################### Dirección #######################
		formDireccion = DireccionForm(request.POST, prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(request.POST, prefix='direccion')
		if has_info(request.POST, prefix='direccion', investigacion=investigacion):
			if formDireccion.is_valid():
				direccion = formDireccion.save(commit=False)
				direccion.persona = investigacion.candidato
				direccion.save()
			else:
				msg_param = ''
		####################### Teléfono1 (casa)  #######################
		formTelefono1 = TelefonoForm(request.POST, prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(request.POST, prefix='telefono1')
		if has_info(request.POST, prefix='telefono1', investigacion=investigacion):
			if formTelefono1.is_valid():
				tel1 = formTelefono1.save(commit=False)
				tel1.persona = investigacion.candidato
				tel1.categoria = 'casa'
				tel1.save()
			else:
				msg_param = ''
		####################### Teléfono2 (movil)  #######################
		formTelefono2 = TelefonoForm(request.POST, prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(request.POST, prefix='telefono2')
		if has_info(request.POST, prefix='telefono2', investigacion=investigacion):
			if formTelefono2.is_valid():
				tel2 = formTelefono2.save(commit=False)
				tel2.persona = investigacion.candidato
				tel2.categoria = 'movil'
				tel2.save()
			else:
				msg_param = ''
		####################### Teléfono3 (recado)  #######################
		formTelefono3 = TelefonoForm(request.POST, prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(request.POST, prefix='telefono3')
		if has_info(request.POST, prefix='telefono3', investigacion=investigacion):
			if formTelefono3.is_valid():
				tel3 = formTelefono3.save(commit=False)
				tel3.persona = investigacion.candidato
				tel3.categoria = 'recado'
				tel3.save()
			else:
				msg_param = ''
		####################### PrestacionVivienda Infonavit #######################
		formPrestacionViviendaInfonavit = PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit')
		if has_info(request.POST, prefix='prestacion_vivienda_infonavit', investigacion=investigacion):
			if formPrestacionViviendaInfonavit.is_valid():
				prestacionViviendaInfonavit = formPrestacionViviendaInfonavit.save(commit=False)
				prestacionViviendaInfonavit.persona = investigacion.candidato
				prestacionViviendaInfonavit.categoria_viv = 'infonavit'
				prestacionViviendaInfonavit.save()
			else:
				msg_param = ''
		####################### PrestacionVivienda Fonacot #######################
		formPrestacionViviendaFonacot = PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot')
		if has_info(request.POST, prefix='prestacion_vivienda_fonacot', investigacion=investigacion):
			if formPrestacionViviendaFonacot.is_valid():
				prestacionViviendaFonacot = formPrestacionViviendaFonacot.save(commit=False)
				prestacionViviendaFonacot.persona = investigacion.candidato
				prestacionViviendaFonacot.categoria_viv = 'fonacot'
				prestacionViviendaFonacot.save()
			else:
				msg_param = ''
		####################### Legalidad #######################
		formLegalidad = LegalidadAltaForma(request.POST, prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(request.POST, prefix='legalidad')
		if has_info(request.POST, prefix='legalidad', investigacion=investigacion):
			if formLegalidad.is_valid():
				legalidad = formLegalidad.save(commit=False)
				legalidad.persona = investigacion.candidato
				legalidad.save()
			else:
				msg_param = ''

		####################### Demanda
		formDemanda = DemandaFormSet(request.POST)

		####################### Seguro #######################
		formSeguro = SeguroAltaForma(request.POST, prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(request.POST, prefix='seguro')
		if has_info(request.POST, prefix='seguro', investigacion=investigacion):
			if formSeguro.is_valid():
				seguro = formSeguro.save(commit=False)
				seguro.persona = investigacion.candidato
				seguro.save()
			else:
				msg_param = ''

		####################### Investigación #######################

		formSucursal = CompaniaSucursalForm(request.POST.get('investigacion-compania'), request.POST.get('investigacion-sucursal'), prefix='investigacion')

		formInvestigacion = InvestigacionEditarForm(request.POST, prefix='investigacion', instance=investigacion, agt_id=agente_id)
		if request.POST.get('investigacion-sucursal', '') == '':
			msg.append('Es necesario seleccionar sucursal')
			status = 'danger'
		elif not formInvestigacion.is_valid():
			msg_param = ''
		else:
			####################### Demanda
			if formDemanda.is_valid():
				for formItem in formDemanda:
					demanda = formItem.save(commit=False)
					demanda.persona = investigacion.candidato
					demanda.save()
			else:
				msg_param = formDemanda.errors

			investigacion = formInvestigacion.save()
			investigacion.status_active = True

			investigacion.save()

			if Cobranza.objects.filter(investigacion=investigacion).count() == 0:
				Cobranza(investigacion=investigacion).save()

			if msg_param != '':
				if 'guardar_sucursal' in request.POST:
					return HttpResponseRedirect('/empresa/' + str(investigacion.compania.id) + '/sucursales?investigacion=' + str(investigacion.id))
				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))
				return HttpResponseRedirect('/candidato/investigacion/'+str(investigacion_id)+'/editar'+msg_param)

	else:
		formCandidato = CandidatoAltaForm(prefix='candidato', instance=investigacion.candidato)
		formInvestigacion = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={'compania' : investigacion.compania.id }, agt_id=agente_id)
		formOrigen = OrigenAltaForma(prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(prefix='origen')		
		formDireccion = DireccionForm(prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(prefix='direccion')
		formTelefono1 = TelefonoForm(prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(prefix='telefono1')
		formTelefono2 = TelefonoForm(prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(prefix='telefono2')
		formTelefono3 = TelefonoForm(prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(prefix='telefono3')
		formPrestacionViviendaInfonavit = PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit')
		formPrestacionViviendaFonacot = PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot')
		formLegalidad = LegalidadAltaForma(prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(prefix='legalidad')		
		formDemanda = DemandaFormSet(queryset=Demanda.objects.filter(persona=investigacion.candidato))
		formSeguro = SeguroAltaForma(prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(prefix='seguro')
		formSucursal = CompaniaSucursalForm(investigacion.compania.id, investigacion.sucursal.id if investigacion.sucursal else None, prefix='investigacion')

		# FORMAS QUE FALTAN POR EDITAR
		formTrayectoria1 = TrayectoriaForm(prefix='trayectoria1')
		formEvaluacion1 = EvaluacionForm(prefix='evaluacion1')
		formOpinionJefe = OpinionAltaForma(prefix='opinion_jefe')
		formOpinionRH = OpinionAltaForma(prefix='opinion_rh')
		formInformante1 = InformanteAltaForma(prefix='informante1')
		formInformante2 = InformanteAltaForma(prefix='informante2')

	return render(request, 'sections/candidato/editar.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def eliminar(request, investigacion_id):
	i = Investigacion.objects.get(id=investigacion_id)
	i.status_active = False
	i.save()
	b = Bitacora(action='investigacion-eliminada: ' + str(i), user=request.user)
	b.save()
	return HttpResponseRedirect('/candidatos')

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def nueva_trayectoria(request, investigacion_id, empresa_id=''):
	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('-fecha_creacion')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)
	status_list = PersonaService.get_status_list(investigacion_id)

	empresa_creada = Compania.objects.get(pk=empresa_id) if empresa_id else None


	page = 'candidatos'
	seccion = 'trayectoria'	
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(id=investigacion_id)

	if request.method == 'POST':
		if 'cancelar' in request.POST:
			return HttpResponseRedirect('/candidato/investigacion/' + str(investigacion_id) + '/trayectoria')
		formTrayectoria = TrayectoriaFormSoloCompania(request.POST, prefix='trayectoria')
		if formTrayectoria.is_valid():
			nueva_trayectoria = formTrayectoria.save(commit=False)
			nueva_trayectoria.persona = investigacion.candidato
			nueva_trayectoria.save()
			Evaluacion(trayectoriaLaboral=nueva_trayectoria).save()
			b = Bitacora(action='trayectoria-nueva: ' + str(nueva_trayectoria.id) + ', compania: ' + str(nueva_trayectoria.compania.id) + ', investigacion: ' + str(investigacion.id), user=request.user)
			b.save()

			if 'cancelar' in request.POST:
				return HttpResponseRedirect('/candidato/investigacion/' + str(investigacion_id) + '/trayectoria')
			elif 'guardar_capturar' in request.POST:
				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/editar/trayectoria/' + str(nueva_trayectoria.id))
			elif 'guardar_solo' in request.POST:
				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/')

	else:
		formTrayectoria = TrayectoriaFormSoloCompania(prefix='trayectoria')

	return render(request, 'sections/candidato/nueva_trayectoria.html', locals(), RequestContext(request))

### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def ver_trayectoria(request, investigacion_id):
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
	seccion = 'trayectoria'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(id=investigacion_id)
	trayectorias_laborales = investigacion.get_trayectorias_laborales(is_usuario_contacto)
	referencias_comerciales = TrayectoriaComercial.objects.filter(persona=investigacion.candidato)
	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

	is_user_captura = request.user.groups.filter(name="captura").count()

	if request.method == 'POST' and not is_usuario_contacto:
		if 'autogenerar' in request.POST:
			investigacion.observaciones_generales = get_observacion_automatica(trayectorias_laborales)
			investigacion.save()

			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/exito')
		else:
			is_completed = request.POST.get('laboral-completado')
			if is_completed == "on" and not investigacion.fecha_laboral:
				investigacion.fecha_laboral = datetime.datetime.now()
				investigacion.save()

			formaInvestigacion = InvestigacionStatusTrayectoriaForm(request.POST, prefix='investigacion', instance=investigacion)
			if formaInvestigacion.is_valid():
				formaInvestigacion.save()

				if 'redirect' in request.POST:
					return HttpResponseRedirect(request.POST.get('redirect'))

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/exito')
	else:
		formaInvestigacion = InvestigacionStatusTrayectoriaForm(prefix='investigacion', instance=investigacion)
		
	return render(request, 'sections/candidato/trayectoria_panel.html', locals(), RequestContext(request))

### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def editar_trayectoria_empresa(request, investigacion_id, trayectoria_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')

	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)
	status_list = PersonaService.get_status_list(investigacion_id)

	page = 'candidatos'
	seccion = 'trayectoria'
	status = ''
	msg = []
	investigacion = Investigacion.objects.get(id=investigacion_id)
	trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(pk=trayectoria_id)
	evaluacion = trayectoria_empresa.evaluacion_set.all()
	opinion_jefe = trayectoria_empresa.opinion_set.filter(categoria=1) if evaluacion else None 
	opinion_rh = trayectoria_empresa.opinion_set.filter(categoria=2) if evaluacion else None
	carta_laboral = trayectoria_empresa.cartalaboral if hasattr(trayectoria_empresa, 'cartalaboral') else None
	datos_generales = trayectoria_empresa.datosgenerales if hasattr(trayectoria_empresa, 'datosgenerales') else None

	informantes = evaluacion[0].informante_set.all() if evaluacion else None
	informante1 = informantes[0] if informantes else None
	informante2 = (informantes[1] if informantes.count() > 1 else None) if informantes else None

	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)
	formSucursal = CompaniaSucursalForm(trayectoria_empresa.compania.id, trayectoria_empresa.sucursal.id if trayectoria_empresa.sucursal else None, prefix='trayectoria')

	is_user_captura = request.user.groups.filter(name="captura").count()

	if request.method == 'POST' and not is_usuario_contacto:
		exito = True
		if 'cancelar' in request.POST:
			return HttpResponseRedirect('/candidato/investigacion/' + str(investigacion_id) + '/trayectoria')
		
		if 'editar_sucursal' in request.POST:
			return HttpResponseRedirect('/empresa/' + str(trayectoria_empresa.compania.id) + '/sucursales?investigacion=' + str(investigacion.id) + '&trayectoria=' + str(trayectoria_id))
		
		formTrayectoria = TrayectoriaForm(request.POST, prefix='trayectoria', instance=trayectoria_empresa)
		if formTrayectoria.is_valid(): 
			trayectoria_empresa = formTrayectoria.save()
		else:
			logger.info('formTrayectoria invalid')
			exito = False

		############## Carta Laboral
		formCartaLaboral = CartaLaboralForma(request.POST, instance=carta_laboral)
		if formCartaLaboral.is_valid():
			carta_laboral = formCartaLaboral.save(commit=False)
			carta_laboral.trayectoriaLaboral = trayectoria_empresa
			carta_laboral.save()
		else:
			logger.info('formCartaLaboral invalid')
			exito = False
		
		############## Datos Generales
		formDatosGenerales = DatosGeneralesForma(request.POST, instance=datos_generales)
		if formDatosGenerales.is_valid():
			datos_generales = formDatosGenerales.save(commit=False)
			datos_generales.trayectoriaLaboral = trayectoria_empresa
			datos_generales.save()
		else:
			logger.info('formDatosGenerales invalid')
			exito = False

		############## Evaluación ##############
		formEvaluacion = EvaluacionForm(request.POST, prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(request.POST, prefix='evaluacion')
		if has_info_trayectoria(request.POST, prefix='evaluacion', trayectoria=trayectoria_empresa):
			if formEvaluacion.is_valid():
				evaluacion = formEvaluacion.save(commit=False)
				evaluacion.trayectoriaLaboral = trayectoria_empresa
				evaluacion.save()
			else:
				logger.info('formEvaluacion invalid')
				exito = False

		############## Opinion (Jefe) ##############
		formOpinionJefe = OpinionAltaForma(request.POST, prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(request.POST, prefix='opinion_jefe')
		if has_info_trayectoria(request.POST, prefix='opinion_jefe', trayectoria=trayectoria_empresa):
			if formOpinionJefe.is_valid():
				opinion_jefe = formOpinionJefe.save(commit=False)
				opinion_jefe.trayectoriaLaboral = trayectoria_empresa
				opinion_jefe.categoria = 1
				opinion_jefe.save()
			else:
				logger.info('opinion_jefe invalid')
				exito = False

		############## Opinion (RH) ##############
		formOpinionRH = OpinionAltaForma(request.POST, prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(request.POST, prefix='opinion_rh')
		if has_info_trayectoria(request.POST, prefix='opinion_rh', trayectoria=trayectoria_empresa):
			if formOpinionRH.is_valid():
				opinion_rh = formOpinionRH.save(commit=False)
				opinion_rh.trayectoriaLaboral = trayectoria_empresa
				opinion_rh.categoria = 2
				try:
					opinion_rh.save()
				except Exception as error:
					logger.info('opinion_rh error')
					msg.append({
						"text": "Opinion RH: " + str(error),
						"status": "danger"
					})
					exito = False	
			else:
				logger.info('formOpinionRH invalid')
				exito = False

		############## Informantes  ##############
		formInformante1 = InformanteAltaForma(request.POST, prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(request.POST, prefix='informante1')
		if has_info_trayectoria(request.POST, prefix='informante1', trayectoria=trayectoria_empresa):
			informante1 = formInformante1.save(commit=False)
			informante1.evaluacion = evaluacion
			informante1.save()

		formInformante2 = InformanteAltaForma(request.POST, prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(request.POST, prefix='informante2')
		if has_info_trayectoria(request.POST, prefix='informante2', trayectoria=trayectoria_empresa):
			informante2 = formInformante2.save(commit=False)
			informante2.evaluacion = evaluacion
			informante2.save()

		b = Bitacora(action='trayectoria-editar: ' + str(trayectoria_empresa), user=request.user)
		b.save()
		if exito:
			if 'guardar_sucursal' in request.POST:
				return HttpResponseRedirect('/empresa/' + str(trayectoria_empresa.compania.id) + '/sucursal/nueva?investigacion_id=' + investigacion_id + '&trayectoria=' + trayectoria_id)
			
			if 'redirect' in request.POST:
				return HttpResponseRedirect(request.POST.get('redirect'))

			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/editar/trayectoria/'+trayectoria_id+'/exito')

	else:
		formTrayectoria = TrayectoriaForm(prefix='trayectoria', instance=trayectoria_empresa)
		formCartaLaboral = CartaLaboralForma(instance=carta_laboral) if carta_laboral else CartaLaboralForma()
		formDatosGenerales = DatosGeneralesForma(instance=datos_generales) if datos_generales else DatosGeneralesForma()
		formEvaluacion = EvaluacionForm(prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')
		
		#formEvaluacion = EvaluacionForm(prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')
		formOpinionJefe = OpinionAltaForma(prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(prefix='opinion_jefe')
		formOpinionRH = OpinionAltaForma(prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(prefix='opinion_rh')
		formInformante1 = InformanteAltaForma(prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(prefix='informante1')
		formInformante2 = InformanteAltaForma(prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(prefix='informante2')


	return render(request, 'sections/candidato/editar_trayectoria_empresa.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def borrar_trayectoria_empresa(request, investigacion_id, trayectoria_id):
	investigacion = Investigacion.objects.get(id=investigacion_id)
	trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(pk=trayectoria_id)
	trayectoria_empresa.status = False
	trayectoria_empresa.save()

	b = Bitacora(action='trayectoria-borrar: ' + str(trayectoria_empresa), user=request.user)
	b.save()

	return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/')

'''
	Observaciones
'''
### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def observaciones(request, investigacion_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')
	
	is_user_captura = request.user.groups.filter(name="captura").count()

	page = 'candidatos'
	seccion = 'observaciones'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.select_related('compania', 'candidato').get(id=investigacion_id)
	status_list = PersonaService.get_status_list(investigacion_id)	
	entrevista = EntrevistaCita.objects.filter(investigacion=investigacion).order_by('-id')[0] if EntrevistaCita.objects.filter(investigacion=investigacion).count() else None

	cobranza = investigacion.cobranza_set.all()[0] if investigacion.cobranza_set.count() else None
	monto_actual = None
	tiene_factura = False
	tiene_costo = False
	if cobranza:
		monto_actual = cobranza.monto 
		if cobranza.folio:
			tiene_factura = True
		if cobranza.monto:
			tiene_costo = True
	facturas = Factura.objects.filter(investigacion=investigacion) if Factura.objects.filter(investigacion=investigacion).count() else None

	#para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)
	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion, entrevista)

	status_general = investigacion.status_general
	gestor_investigacion = GestorInvestigacion.objects.filter(investigacion=investigacion)
	gestor_investigacion = gestor_investigacion.first() if gestor_investigacion else None

	if request.method == 'POST' and not is_usuario_contacto:
		formaInvestigacion = InvestigacionStatusForm(request.POST, prefix='investigacion', instance=investigacion)
		formaEntrevista = EntrevistaObservacionesForm(request.POST, prefix='entrevista', instance=entrevista) if entrevista else EntrevistaObservacionesForm(request.POST, prefix='entrevista')
		formaGestorInvestigacion = GestorInvestigacionForm(request.POST, prefix='gestor_investigacion', instance=gestor_investigacion) if gestor_investigacion else GestorInvestigacionForm(request.POST, prefix='gestor_investigacion')
		if formaInvestigacion.is_valid() and formaEntrevista.is_valid() and formaGestorInvestigacion.is_valid():
			# GESTOR INVESTIGACION
			formaGestorInvestigacion.instance.fecha_registro = datetime.datetime.now()
			formaGestorInvestigacion.instance.investigacion_id = investigacion.id
			if request.POST.get('gestor_investigacion-estatus') == '2':
				formaGestorInvestigacion.instance.fecha_asignacion = datetime.datetime.now()
				EntrevistaPersonaService(investigacion_id).verifyData()
			if request.POST.get('gestor_investigacion-estatus') == '3':
				formaGestorInvestigacion.instance.fecha_atencion = datetime.datetime.now()
			formaGestorInvestigacion.save()

			#Validación adicional para tipo de investigación
			hasInterview = investigacion.entrevistapersona_set.all().count()
			hasTrayectorias = investigacion.get_trayectorias_laborales(True)

			inv_new_instance = formaInvestigacion.save(commit=False)
			if not request.user.is_superuser and status_general == '2':
				inv_new_instance.status_general = status_general

			if inv_new_instance.status_general == '2':
				if hasInterview > 0 and hasTrayectorias:
					inv_new_instance.tipo_investigacion_status = 2
				elif hasInterview > 0 and hasTrayectorias is False:
					inv_new_instance.tipo_investigacion_status = 5
				elif hasInterview == 0 and hasTrayectorias:
					inv_new_instance.tipo_investigacion_status = 1
			
			inv_new_instance.save()

			formaEntrevista.save()
			if 'redirect' in request.POST:
				return HttpResponseRedirect(request.POST.get('redirect'))

			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/observaciones/exito')		
	else:
		formaInvestigacion = InvestigacionStatusForm(prefix='investigacion', instance=investigacion)
		formaInvestigacion.fields['label'].queryset = Labels.objects.filter(agente=request.user).exclude(name__exact='')
		formaEntrevista = EntrevistaObservacionesForm(prefix='entrevista', instance=entrevista) if entrevista else EntrevistaObservacionesForm(prefix='entrevista')
		formaCobranza = CobranzaMontoForm(prefix='cobranza', instance=cobranza)
		formaGestorInvestigacion = GestorInvestigacionForm(prefix='gestor_investigacion', instance=gestor_investigacion) if gestor_investigacion else GestorInvestigacionForm(prefix='gestor_investigacion')
	return render(request, 'sections/candidato/observaciones.html', locals(), RequestContext(request))

'''
	Reporte
'''
### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def ver_reporte(request, investigacion_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')
		
	page = 'candidatos'
	seccion = 'reporte'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(id=investigacion_id)
	status_list = PersonaService.get_status_list(investigacion_id)
	
	#para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	tiene_trayectoria = True if investigacion.candidato.trayectorialaboral_set.all().count() else False
	tiene_entrevista = True if investigacion.entrevistapersona_set.all().count() else False

	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

	is_user_captura = request.user.groups.filter(name="captura").count()

	return render(request, 'sections/candidato/ver_reporte.html', locals(), RequestContext(request))

'''
	Función que verifica la existencia de uno o más candidatos con los datos enviados por POST (AJAX)
'''
@csrf_exempt
def existencia(request):
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		nss = request.POST.get('nss', '')
		curp = request.POST.get('curp', '')
		investigacion_id = request.POST.get('investigacion_id', '')
		candidato = ''
		if len(nss) > 0 and len(curp) > 0:
			candidato = Persona.objects.filter(Q(nss=nss) | Q(curp=curp))
		elif len(nss) > 0 and len(curp) == 0:
			candidato = Persona.objects.filter(nss=nss)
		elif len(curp) > 0 and len(nss) == 0:
			candidato = Persona.objects.filter(curp=curp)
		
		candidatos_data = []

		if len(candidato):
			ids = []
			for c in candidato:
				datos_generales = {}
				invs_data = []
				ids.append(c.id)
				invs = Investigacion.objects.filter(candidato=c)
				if investigacion_id:
					invs = invs.exclude(id=investigacion_id)

				if invs.count():
					for i in invs:
						invs_data.append({'id': i.id , 'compania' : i.compania.nombre })
					datos_generales = { 'id' : c.id , 
									'nombre' : c.nombre,
									'nss' : c.nss,
									'email' : c.email,
									'edad'  : c.edad,
									'curp' : c.curp
					}
					candidatos_data.append({'datos_generales' : datos_generales , 'investigaciones' : invs_data })
					response = { 'status' : True , 'candidatos' : candidatos_data }
		
	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def search_candidatos(request):	
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		ps = PersonaService(request)
		candidatos = ps.getCandidatosList()
		response = { 'status' : True , 'candidatos' : candidatos }	
	return JsonResponse(response)

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')

@login_required(login_url='/login', redirect_field_name=None)
def trayectoria_comercial(request, investigacion_id, trayectoria_id=None):
	if not request.user.is_staff and request.user.groups.filter(name="captura").count() == 0:
		return HttpResponseRedirect('/')
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	filtros_json = request.session.get('filtros_search', None)

	page = 'candidatos'
	seccion = 'trayectoria'	
	
	investigacion = Investigacion.objects.get(id=investigacion_id)
	trayectoria_instance = TrayectoriaComercial.objects.get(id=trayectoria_id) if trayectoria_id else None
	
	referencia_extra = 3 - TrayectoriaComercialReferencia.objects.filter(trayectoria_comercial=trayectoria_id).count() if trayectoria_id else 3
	referencia_formset = modelformset_factory(TrayectoriaComercialReferencia, form=TrayectoriaComercialReferenciaForm, extra=referencia_extra)

	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False

	if request.method == 'POST':
		trayectoria_comercial_form = TrayectoriaComercialForm(request.POST, instance=trayectoria_instance)
		trayectoria_comercial_referencia_formset = referencia_formset(request.POST)

		if trayectoria_comercial_form.is_valid():
			trayectoria_comercial = trayectoria_comercial_form.save(commit=False)
			trayectoria_comercial.persona = investigacion.candidato
			trayectoria_comercial.save()

			if trayectoria_comercial_referencia_formset.is_valid():
				trayectoria_comercial_referencia = trayectoria_comercial_referencia_formset.save(commit=False)
				for referencia in trayectoria_comercial_referencia:
					referencia.trayectoria_comercial = trayectoria_comercial
					referencia.save()
				
				b = Bitacora(action='trayectoria_comercial: ' + str(trayectoria_id), user=request.user)
				b.save()

				return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/exito')
	else:
		trayectoria_comercial_form = TrayectoriaComercialForm(instance=trayectoria_instance)
		
		referencial_queryset = TrayectoriaComercialReferencia.objects.filter(trayectoria_comercial=trayectoria_id) if trayectoria_id else TrayectoriaComercialReferencia.objects.none()
		trayectoria_comercial_referencia_formset = referencia_formset(queryset=referencial_queryset)

	return render(request, 'sections/candidato/trayectoria_comercial.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def trayectoria_comercial_borrar(request, investigacion_id, trayectoria_id):
	trayectoria = TrayectoriaComercial.objects.get(id=trayectoria_id)
	trayectoria.delete()

	b = Bitacora(action='trayectoria_comercial-borrar: ' + str(trayectoria_id), user=request.user)
	b.save()

	return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/')

@login_required(login_url='/login', redirect_field_name=None)
def trayectoria_comercial_referencia_borrar(request, investigacion_id, trayectoria_id, referencia_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	if is_usuario_contacto:
		return HttpResponseRedirect('/')

	trayectoria_comercial_referencia = TrayectoriaComercialReferencia.objects.get(id=referencia_id)
	trayectoria_comercial_referencia.delete()

	b = Bitacora(action='trayectoria_comercial_referencia-borrar: ' + str(referencia_id), user=request.user)
	b.save()

	return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/trayectoria/')

def borrar_demanda(request, investigacion_id, demanda_id):
	if demanda_id:
		Demanda.objects.get(id=demanda_id).delete()
	return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/editar/exito')
