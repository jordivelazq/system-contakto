# -*- coding: utf-8 -*-
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
from app.cobranza.forms import CobranzaMontoForm, FacturaForm, FacturaInvestigacionForm
from app.cobranza.services import get_cobranza, get_cobranza_csv_row, get_investigaciones, get_total_investigaciones_facturadas, get_cobranza_filters, get_cobranza_csv_row_2
from app.util.forms import FiltersForm
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from app.entrevista.controllerpersona import ControllerPersona
from app.persona.form_functions import *
from app.util.cobranza_upload import cobranza_upload
from django.conf import settings
from calendar import monthrange
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

	(start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio) = get_cobranza_filters(request, filtros_json)

	investigaciones = get_investigaciones(False, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio)
	total_investigaciones = get_investigaciones(True, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio)
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
			today = datetime.datetime.today()
			date_from = datetime.date.today().replace(day=1)
			date_to = datetime.date.today().replace(day=monthrange(today.year, today.month)[1])

			facturas = facturas.filter(fecha__gte=date_from, fecha__lte=date_to)
			filters_form = FiltersForm({
				'date_from': date_from.strftime("%d/%m/%y"),
			'date_to': date_to.strftime("%d/%m/%y")
			})
		else:
			filters_form = FiltersForm(request.POST)
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
			
			name = request.POST.get('name', '')
			if name:
				facturas = facturas.filter(nombre__icontains=name)
	else:
		today = datetime.datetime.today()
		date_from = datetime.date.today().replace(day=1)
		date_to = datetime.date.today().replace(day=monthrange(today.year, today.month)[1])

		facturas = facturas.filter(fecha__gte=date_from, fecha__lte=date_to)
		filters_form = FiltersForm({
			'date_from': date_from.strftime("%d/%m/%y"),
			'date_to': date_to.strftime("%d/%m/%y")
		})

	facturas = facturas.all().order_by('fecha', 'folio')[:500]	

	return render(request, 'sections/cobranza/facturas.html', {
		"page": page,
		"facturas": facturas,
		"request": request,
		"total_facturas": total_facturas,
		"filters_form": filters_form
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

	(start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio) = get_cobranza_filters(request, filtros_json)

	rows = get_investigaciones(False, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio)
	header = ('ID', 'FECHA DE RECIBIDO', 'CLIENTE', 'NOMBRE', 'APELLIDO', 'PUESTO', 'ESTADO', 'MONTO', 'FOLIO', 'CORREO', 'SOLICITANTE', 'SOCIAL', 'EJECUTIVO', 'OBS. COBRANZA', 'TIPO INV.', 'ESTATUS', 'RESULTADO', 'OBS .INVESTIGACION', '')
	rows = (header,) + rows

	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)

	response = StreamingHttpResponse((writer.writerow(get_cobranza_csv_row_2(row)) for row in rows), content_type="text/csv")
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
		folio = request.POST.get('folio', '')

		request.session['filtros_search_cobranza'] = {
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'contacto_id':contacto_id, 
			'factura_folio':factura_folio, 
			'status_id':status_id,
			'agente_select': agente_select,
			'fecha_inicio':fecha_inicio,
			'fecha_final':fecha_final,
			'folio':folio
		}

		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_cobranza'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')
