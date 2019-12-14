# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
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
	'''
		NOTA: Al modificar código en esta función, revisar también app.reportes.servcies, pues ahí también
		se generan los reportes que se envian por correo. El código es similar.
	'''
	#Fix por pixeles en Chrome (input-group-addon de bootstrap)
	es_chrome = 'Chrome' in request.META['HTTP_USER_AGENT']
	page = 'reportes'
	service_reporte = ServiceReporte()

	#para SEARCH sidebar
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	status_select = PersonaService.STATUS_GRAL_OPCIONES_SIDEBAR
	status_laboral_select = Investigacion.STATUS_OPCIONES
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='admint')
	filtros_json = request.session.get('filtros_search_reportes', None)
	
	if request.POST:
		investigaciones = request.POST.getlist('investigacion[]')
		destinatarios = request.POST.get('destinatarios')
		user = request.user
		if service_reporte.send_reporte_by_email(investigaciones, destinatarios, user):
			return HttpResponseRedirect('/estatus/exito')
		else:
			return HttpResponseRedirect('/estatus/error')
	
	if filtros_json != None:
		if (not len(filtros_json['compania_id']) 
		and not len(filtros_json['compania_nombre']) 
		and not len(filtros_json['contacto_id']) 
		and not len(filtros_json['status_id'])
		and ('status_laboral_id' not in filtros_json or not len(filtros_json['status_laboral_id'])) 
		and not len(filtros_json['fecha_inicio']) 
		and not len(filtros_json['fecha_final']) 
		and not len(filtros_json['agente_id'])):
			recientes = True

		if 'contacto_id' in filtros_json and len(filtros_json['contacto_id']):
			contacto_id = filtros_json['contacto_id']
			contacto = Contacto.objects.get(id=contacto_id)
			dest_list = service_reporte.getDestinatarios(request,contacto_id)

		if len(filtros_json['compania_id']):
			compania_id = filtros_json['compania_id']
			compania = Compania.objects.get(id=compania_id)	
	else:
		user = request.user
		if user.groups.filter(name='contactos').count():
			contact = Contacto.objects.get(email=user.username)
			filtros_json = {
				"nombre": "",
				"compania_id": "",
				"compania_nombre": "",
				"contacto_id": str(contact.id),
				"status_id": "",
				"status_laboral_id": "",
				"fecha_inicio": "",
				"agente_id": ""
			}
		recientes = True

	is_agent = request.user.is_staff and not request.user.is_superuser
	investigaciones = get_investigaciones_list(filtros_json, request.user.id if is_agent else None)

	for i in investigaciones:
		i.ciudad = i.candidato.direccion_set.all()[0].ciudad
		i.estado = i.candidato.direccion_set.all()[0].estado
		i.entrevista = i.entrevistacita_set.all()[0] if i.entrevistacita_set.all().count() else None
		i.trayectoria = i.candidato.trayectorialaboral_set.filter(visible_en_status=True, status=True)
			
	return render_to_response('sections/reportes/panel.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def exportar_pdf(request):
	filtros_json = request.session.get('filtros_search_reportes', None)
	investigaciones = get_investigaciones_list(filtros_json)

	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="reporte_investigaciones_cliente.pdf"'

	# Create the PDF object, using the response object as its "file."
	p = canvas.Canvas(response)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	
	content = ''
	c = 1
	for i in investigaciones:
		content = unicode(i.compania.nombre)+' / '+unicode(i.candidato.nombre)+' / '+unicode(i.puesto)
		p.drawString(80, 750-c, content)
		c=c+15

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()
	return response

@csrf_exempt
def search_reportes(request):
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		nombre = request.POST.get('nombre', '')
		compania_id = request.POST.get('compania_id', '')
		compania_nombre = request.POST.get('compania_nombre', '')
		contacto_id = request.POST.get('contacto_id', '')
		status_id = request.POST.get('status_id', '')
		status_laboral_id = request.POST.get('status_laboral_id', '')
		fecha_inicio = request.POST.get('fecha_inicio', '')
		fecha_final = request.POST.get('fecha_final', '')
		agente_id = request.POST.get('agente_id', '')
		
		request.session['filtros_search_reportes'] = {
			'nombre': nombre, 
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'contacto_id':contacto_id, 
			'status_id':status_id, 
			'status_laboral_id': status_laboral_id,
			'fecha_inicio':fecha_inicio,
			'fecha_final':fecha_final, 
			'agente_id': agente_id
		}
		 
		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_reportes'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')

def get_investigaciones_list(filtros_json, agent_id):
	investigaciones = Investigacion.objects.filter(status_active=True).order_by('fecha_recibido')

	if agent_id:
		investigaciones = investigaciones.filter(agente_id=agent_id)

	if filtros_json != None:
		if (not len(filtros_json['nombre'])
			and not len(filtros_json['compania_id']) 
			and not len(filtros_json['compania_nombre']) 
			and not len(filtros_json['agente_id']) 
			and not len(filtros_json['contacto_id']) 
			and not len(filtros_json['status_id']) 
			and ('status_laboral_id' not in filtros_json or not len(filtros_json['status_laboral_id']))
			and not len(filtros_json['fecha_inicio']) 
			and not len(filtros_json['fecha_final'])):
			recientes = True
			investigaciones = investigaciones.order_by('fecha_recibido')[:50]

		else:
			if len(filtros_json['nombre']):
				investigaciones = investigaciones.filter(Q(candidato__nombre__icontains=filtros_json['nombre'])|Q(candidato__apellido__icontains=filtros_json['nombre']))
			if len(filtros_json['compania_id']):
				investigaciones = investigaciones.filter(compania__id=filtros_json['compania_id'])

			if 'contacto_id' in filtros_json and len(filtros_json['contacto_id']):
				investigaciones = investigaciones.filter(contacto__id=filtros_json['contacto_id'])

			if len(filtros_json['status_id']):
				if filtros_json['status_id'] != '3':
					investigaciones = investigaciones.filter(status_general=filtros_json['status_id'])
				else:
					investigaciones = investigaciones.filter(Q(status_general=0)|Q(status_general=1))
			
			if 'status_laboral_id' in filtros_json and len(filtros_json['status_laboral_id']):
				investigaciones = investigaciones.filter(status=filtros_json['status_laboral_id'])
			
			if len(filtros_json['agente_id']):
				investigaciones = investigaciones.filter(agente__id=filtros_json['agente_id'])

			if len(filtros_json['fecha_inicio']) and len(filtros_json['fecha_final']):
				fecha_inicio_format = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')
				fecha_final_format = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
				investigaciones = investigaciones.filter(fecha_recibido__range=(fecha_inicio_format, fecha_final_format))

	else:
		recientes = True
		investigaciones = investigaciones.order_by('fecha_recibido')[:20]

	return investigaciones
