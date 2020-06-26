# -*- coding: utf-8 -*-
from calendar import monthrange
from django.shortcuts import HttpResponse, render
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.six.moves import range
from django.http import StreamingHttpResponse

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
from app.cobranza.models import Cobranza, Factura
from app.cobranza.forms import CobranzaMontoForm, FacturaForm, FacturaInvestigacionForm, FacturaFilters
from app.cobranza.services import get_cobranza, get_cobranza_csv_row, get_investigaciones, get_total_investigaciones_facturadas
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from app.util.cobranza_upload import cobranza_upload
from django.conf import settings
import datetime
import xlrd
import os
import json
import csv
import subprocess

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def panel(request):
	messages = []

	if request.method == 'POST' and 'importar' in request.POST:
		form_file = EntrevistaFileForm(request.POST, request.FILES)

		if form_file.is_valid():
			ext = os.path.splitext(str(request.FILES['record']))[1]

			if ext.lower() not in settings.EXT_RESEARCH_WHITELIST:
				messages = [{
					"msg": "Es necesario cargar archivo de excel",
					"type": "danger"
				}]
			else:
				file_instance = EntrevistaFile(record=request.FILES['record'], tipo=2)
				file_instance.save()

				cobranza_upload(file_instance.record.path)

				return HttpResponseRedirect('/cobranza/exito')
	else:
		form_file = EntrevistaFileForm()

	page = 'cobranza'
	
	#para SEARCH sidebar
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	filtros_json = request.session.get('filtros_search_cobranza', None)
	status_select = Investigacion.STATUS_GRAL_OPCIONES
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com')

	total_cobranza = Investigacion.objects.count()
	today = datetime.datetime.today()
	start_date = datetime.date.today().replace(day=1)
	end_date = datetime.date.today().replace(day=monthrange(today.year, today.month)[1])
	compania_id = None
	contacto_id = None
	agente_id = None
	factura_filter = None
	status = None

	if filtros_json:
		if 'fecha_inicio' in filtros_json and len(filtros_json['fecha_inicio']):
			start_date = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')

		if 'fecha_final' in filtros_json and len(filtros_json['fecha_final']):
			end_date = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
		
		if 'compania_id' in filtros_json and len(filtros_json['compania_id']):
			compania_id = filtros_json['compania_id']
		
		if 'contacto_id' in filtros_json and len(filtros_json['contacto_id']):
			contacto_id = filtros_json['contacto_id']
		
		if 'agente_select' in filtros_json and len(filtros_json['agente_select']):
			agente_id = filtros_json['agente_select']
		
		if 'factura_folio' in filtros_json and len(filtros_json['factura_folio']):
			factura_filter = filtros_json['factura_folio']
		
		if 'status_id' in filtros_json and len(filtros_json['status_id']) and int(filtros_json['status_id']) > -1:
			status = filtros_json['status_id']

	investigaciones = get_investigaciones(False, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status)
	total_investigaciones = get_investigaciones(True, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status)
	total_facturadas = get_total_investigaciones_facturadas()

	facturas_desglose = {
		"total": total_cobranza,
		"facturas": total_facturadas[0],
		"sin_factura": total_cobranza - total_facturadas[0]
	}
	
	return render(request, 'sections/cobranza/panel.html', locals(), RequestContext(request))

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def cobranza_facturas(request):
	facturas = Factura.objects
	total_facturas = Factura.objects.count()
	page = 'cobranza'
	if request.method == 'POST':
		option = request.POST.get('option', '')
		if option == 'Limpiar':
			filters = FacturaFilters()
		else:
			filters = FacturaFilters(request.POST)
			date_a = request.POST.get('date_from', '')
			date_b = request.POST.get('date_to', '')

			date_from = datetime.datetime.strptime(date_a, '%d/%m/%y').strftime('%Y-%m-%d') if date_a else None
			date_to = datetime.datetime.strptime(date_b, '%d/%m/%y').strftime('%Y-%m-%d') if date_b else None

			if date_from and date_to:
				facturas = facturas.filter(fecha__gte=date_from, fecha__lte=date_to)
			elif date_from:
				facturas = facturas.filter(fecha__gte=date_from)
			elif date_to:
				facturas = facturas.filter(fecha__lte=date_to)
	else:
		filters = FacturaFilters()

	facturas = facturas.all().order_by('fecha', 'folio')[:500]	

	return render(request, 'sections/cobranza/facturas.html', {
		"page": page,
		"facturas": facturas,
		"request": request,
		"total_facturas": total_facturas,
		"filters": filters
	}, RequestContext(request))

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def cobranza_investigacion(request, folio = None):
	factura = Factura.objects.get(folio=folio) if folio and Factura.objects.filter(folio=folio).count() else None

	if request.method == 'POST':
		facturaForm = FacturaForm(request.POST, instance = factura)
		if facturaForm.is_valid():
			factura = facturaForm.save()
			
			if folio:
				for investigacion in factura.investigacion.all():
					factura.investigacion.remove(investigacion)

			for investigacion_id in request.POST.get('investigaciones', '').split('\n'):
				if investigacion_id and len(investigacion_id.strip()) > 0:
					investigacion = Investigacion.objects.filter(id=investigacion_id.strip())
					if investigacion.count():
						factura.investigacion.add(investigacion[0])

			return HttpResponseRedirect('/cobranza/facturas/exito')
	else:
		facturaForm = FacturaForm(instance = factura)

	return render(request, 'sections/cobranza/investigacion.html', {
		"facturaForm": facturaForm,
		"request": request,
		"folio": folio,
		"factura": factura
	}, RequestContext(request))

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def eliminar_cobranza_investigacion(request, folio):
	factura = Factura.objects.get(folio=folio)
	factura.delete()

	b = Bitacora(action='factura-eliminada: ' + folio, user=request.user)
	b.save()

	return HttpResponseRedirect('/cobranza/facturas/exito')

class Echo(object):
	"""An object that implements just the write method of the file-like
	interface.
	"""
	def write(self, value):
			"""Write the value by returning it, instead of storing in a buffer."""
			return value

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def generar_reporte(request):
	start_time = time.time()
	filtros_json = request.session.get('filtros_search_cobranza', None)
	rows = get_cobranza(filtros_json, 10000)
	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)
	response = StreamingHttpResponse((writer.writerow(get_cobranza_csv_row(row)) for row in rows[0]), content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="cobranza.csv"'
	duration = time.time() - start_time
	print ("generar_reporte duration", int(duration * 1000))
	return response

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
		fecha_inicio = request.POST.get('fecha_inicio', '')
		fecha_final = request.POST.get('fecha_final', '')

		request.session['filtros_search_cobranza'] = {
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'contacto_id':contacto_id, 
			'factura_folio':factura_folio, 
			'status_id':status_id,
			'agente_select': agente_select,
			'fecha_inicio':fecha_inicio,
			'fecha_final':fecha_final
		}

		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_cobranza'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')
