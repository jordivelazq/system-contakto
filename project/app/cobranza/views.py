# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render_to_response, render
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
from app.cobranza.models import *
from app.cobranza.forms import CobranzaMontoForm, FacturaForm, FacturaInvestigacionForm
from app.cobranza.services import get_cobranza, get_cobranza_csv_row
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

	cobranza, total_cobranza = get_cobranza(filtros_json)

	facturas_desglose = {
		"total": Cobranza.objects.filter(investigacion__status_active=True).count(),
		"facturas": Cobranza.objects.filter(investigacion__status_active=True).exclude(folio__exact='').count(),
		"sin_factura": Cobranza.objects.filter(investigacion__status_active=True).filter(folio__exact='').count()
	}
	
	return render(request, 'sections/cobranza/panel.html', locals(), RequestContext(request))

login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def cobranza_investigacion(request):
	FacturaFormSet = modelformset_factory(Factura, form=FacturaInvestigacionForm, max_num=5, extra=0)

	if request.method == 'POST':
		facturaForm = FacturaForm(request.POST)
		folioForm = FacturaFormSet(request.POST)
		if facturaForm.is_valid():
			factura = facturaForm.save()
				
			for folio in folioForm:
				investigacion_id = folio['folio'].value()
				if investigacion_id:
					investigacion = Investigacion.objects.filter(id=investigacion_id)
					if investigacion.count():
						factura.investigacion.add(investigacion[0])

			return HttpResponseRedirect('/cobranza/exito')

	else:
		facturaForm = FacturaForm()
		folioForm = FacturaFormSet(queryset=Factura.objects.none())


	return render(request, 'sections/cobranza/investigacion.html', {
		"folioForm": folioForm,
		"facturaForm": facturaForm,
	}, RequestContext(request))

class Echo(object):
	"""An object that implements just the write method of the file-like
	interface.
	"""
	def write(self, value):
			"""Write the value by returning it, instead of storing in a buffer."""
			return value

def descargar():
	cobranza = get_cobranza(None, 10000)

	with open('./project/resources/csv/cobranza.csv', mode='w') as cobranza_file:
		writer = csv.writer(cobranza_file, delimiter=',')
		writer.writerow(['ID', 'Fecha de Recibido', 'Cliente', 'Nombre', 'Apellido', 'Puesto', 'Ciudad', 'Monto', 'Folio', 'Correo', 'Solicitante', 'Social', 'Ejecutivo', 'Obs. Cobranza', 'Tipo inv.', 'Estatus', 'Resultado', 'Obs .Investigacion'])
		for cob in cobranza[0].iterator():
			writer.writerow(get_cobranza_csv_row(cob))

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
	print "generar_reporte duration", int(duration * 1000)
	return response

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
	return HttpResponse(json.dumps(response), content_type='application/json')

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
