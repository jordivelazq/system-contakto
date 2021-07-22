# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response, render
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from app.investigacion.models import * 
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from app.compania.models import Contacto

from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from app.persona.services import PersonaService
from django.conf import settings
import datetime
import xlrd
import os
import json
from django.db.models import Q
from app.reportes.services import ServiceReporte
from reportlab.pdfgen import canvas

login_required(login_url='/login', redirect_field_name=None)
def panel(request):
	page = 'reportes'	# use for main_menu.active
	service_reporte = ServiceReporte()

	#para SEARCH sidebar
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	status_laboral_select = Investigacion.STATUS_OPCIONES
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')
	filtros_json = request.session.get('filtros_search_reportes', None)

	contacto_id = None
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	if is_usuario_contacto and Contacto.objects.filter(email=request.user.email, status=True).count():
		contacto_id = Contacto.objects.filter(email=request.user.email)[0].id
	
	if request.POST:
		investigaciones = request.POST.getlist('investigacion[]')
		destinatarios = request.POST.get('destinatarios')
		user = request.user
		if service_reporte.send_reporte_by_email(investigaciones, destinatarios):
			return HttpResponseRedirect('/estatus/exito')
		else:
			return HttpResponseRedirect('/estatus/error')
	
	if filtros_json != None:
		if 'contactos_selected' in filtros_json and len(filtros_json['contactos_selected']):
			contactos_selected = filtros_json['contactos_selected'].split(',')
			dest_list = service_reporte.getDestinatarios(request, contactos_selected)

	investigaciones = get_investigaciones_extended(request, contacto_id)
			
	return render(request, 'sections/reportes/panel.html', locals(), RequestContext(request))

login_required(login_url='/login', redirect_field_name=None)
def reporte_prueba(request):
	return render(request, 'sections/reportes/prueba.html', { "request": request}, RequestContext(request))

@csrf_exempt
def search_reportes(request):
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		nombre = request.POST.get('nombre', '')
		compania_id = request.POST.get('compania_id', '')
		compania_nombre = request.POST.get('compania_nombre', '')
		contactos_selected = request.POST.get('contactos_selected', '')
		status_id = request.POST.get('status_id', '')
		status_laboral_id = request.POST.get('status_laboral_id', '')
		fecha_inicio = request.POST.get('fecha_inicio', '')
		fecha_final = request.POST.get('fecha_final', '')
		agente_id = request.POST.get('agente_id', '')
		limit_select = request.POST.get('limit_select', '')
		
		request.session['filtros_search_reportes'] = {
			'nombre': nombre, 
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'contactos_selected':contactos_selected, 
			'status_id':status_id, 
			'status_laboral_id': status_laboral_id,
			'fecha_inicio':fecha_inicio,
			'fecha_final':fecha_final, 
			'agente_id': agente_id,
			'limit_select': limit_select
		}
		 
		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_reportes'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')

def get_investigaciones_list(filtros_json, agent_id, contacto_id):
	limit_select = 50
	investigaciones = Investigacion.objects.filter(status_active=True)

	if contacto_id:
		investigaciones = investigaciones.filter(contacto__id=contacto_id)
	elif agent_id:
		investigaciones = investigaciones.filter(agente_id=agent_id)
	

	if filtros_json != None:
		if len(filtros_json['nombre']):
			investigaciones = investigaciones.filter(Q(candidato__nombre__icontains=filtros_json['nombre'])|Q(candidato__apellido__icontains=filtros_json['nombre']))

		if len(filtros_json['compania_id']):
			investigaciones = investigaciones.filter(compania__id=filtros_json['compania_id'])

		if 'contactos_selected' in filtros_json and len(filtros_json['contactos_selected']):
			contacto_ids = filtros_json['contactos_selected'].split(',')
			investigaciones = investigaciones.filter(contacto__id__in=contacto_ids)

		if len(filtros_json['status_id']):
			if filtros_json['status_id'] != '3':
				investigaciones = investigaciones.filter(status_general=filtros_json['status_id'])
			else:
				investigaciones = investigaciones.filter(Q(status_general=0)|Q(status_general=1))
		
		if 'status_laboral_id' in filtros_json and len(filtros_json['status_laboral_id']):
			investigaciones = investigaciones.filter(status=filtros_json['status_laboral_id'])
		
		if len(filtros_json['agente_id']):
			investigaciones = investigaciones.filter(agente__id=filtros_json['agente_id'])

		fecha_inicio = None
		fecha_final = None
		if len(filtros_json['fecha_inicio']):
			fecha_inicio = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')
		if len(filtros_json['fecha_final']):
			fecha_final = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')

		if fecha_inicio and fecha_final:
			investigaciones = investigaciones.filter(fecha_recibido__gte=fecha_inicio, fecha_recibido__lte=fecha_final)
		elif fecha_inicio:
			investigaciones = investigaciones.filter(fecha_recibido__gte=fecha_inicio)
		elif fecha_final:
			investigaciones = investigaciones.filter(fecha_recibido__lte=fecha_final)

		if 'limit_select' in filtros_json and len(filtros_json['limit_select']):
			limit_select = int(filtros_json['limit_select'])

	investigaciones = investigaciones.order_by('-fecha_recibido')[:limit_select]

	return investigaciones

def get_investigaciones_extended(request, contacto_id):
	filtros_json = request.session.get('filtros_search_reportes', None)

	is_agent = request.user.is_staff and not request.user.is_superuser

	investigaciones = get_investigaciones_list(filtros_json, request.user.id if is_agent else None, contacto_id)

	for i in investigaciones:
		i.ciudad = i.candidato.direccion_set.all()[0].ciudad
		i.estado = i.candidato.direccion_set.all()[0].estado
		i.entrevista = i.entrevistacita_set.all()[0] if i.entrevistacita_set.all().count() else None
		i.trayectoria = i.candidato.trayectorialaboral_set.filter(visible_en_status=True, status=True)
	
	return investigaciones
