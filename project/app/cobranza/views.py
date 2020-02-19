# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
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
from app.cobranza.models import *
from app.cobranza.forms import *
from app.cobranza.services import get_cobranza
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from django.conf import settings
import datetime
import xlrd
import os
import json
from django.db.models import Q

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def panel(request):
	#Operaciones de panel (Agregar/Quitar factura)
	if request.method == 'POST':
		selection = request.POST.get('selection_json', '').split(',')
		if len(selection):
			folio_nuevo = request.POST.get('num_factura','') if 'agregar_factura' in request.POST else ''
			for fact_id in selection:
				c = Cobranza.objects.get(id=fact_id)
				if not c.folio or folio_nuevo == '':
					c.folio = folio_nuevo
					c.save()

			return HttpResponseRedirect('/cobranza/exito')

	page = 'cobranza'
	
	#para SEARCH sidebar
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	filtros_json = request.session.get('filtros_search_cobranza', None)
	status_select = Investigacion.STATUS_GRAL_OPCIONES
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')

	cobranza = get_cobranza(filtros_json)
	
	return render_to_response('sections/cobranza/panel.html', locals(), context_instance=RequestContext(request))

'''
	AJAX
'''
@login_required(login_url='/login', redirect_field_name=None)
def get_facturas(request, compania_id='', contacto_id=''):
	response = {'status': False}
	facturas = Cobranza.objects.filter(investigacion__status_active=True)

	if compania_id and contacto_id:
		facturas = facturas.filter(investigacion__compania__id=compania_id, investigacion__contacto__id=contacto_id)
	elif compania_id:
		facturas = facturas.filter(investigacion__compania__id=compania_id)
	elif contacto_id:	
		facturas = facturas.filter(investigacion__contacto__id=contacto_id)

	if facturas.count():
		facturas = facturas.order_by('folio').values_list('folio', flat=True).distinct()
		data = []
		for f in facturas:
			if f:#OPTIMIZAR con exlude en query
				data.append(f)
		response = {'status': True, 'facturas': data}
	return HttpResponse(json.dumps(response), mimetype='application/json')

@csrf_exempt
def search_cobranza(request):
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		compania_id = request.POST.get('compania_id', '')
		compania_nombre = request.POST.get('compania_nombre', '')
		contacto_id = request.POST.get('contacto_id', '')
		factura_folio = request.POST.get('factura_folio', '')
		status_id = request.POST.get('status_id', '')
		agente_select = request.POST.get('agente_select', '')

		request.session['filtros_search_cobranza'] = {
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'contacto_id':contacto_id, 
			'factura_folio':factura_folio, 
			'status_id':status_id,
			'agente_select': agente_select
		}

		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_cobranza'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')
