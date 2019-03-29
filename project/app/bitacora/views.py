# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def panel(request):
	if not request.user.is_superuser:
		return HttpResponseRedirect('/panel')

	page = 'bitacora'
	ultimos_dias = 30
	bitacoras = Bitacora.objects.all().order_by('-id')

	#para SEARCH sidebar
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='admin').order_by('username')
	filtros_json = request.session.get('filtros_search_bitacora', None)

	if filtros_json != None:
		if not len(filtros_json['agente_id']) and not len(filtros_json['fecha_inicio']) and not len(filtros_json['fecha_final']):
			#DEFAULT
			recientes = True
			bitacoras = bitacoras.filter(datetime__range=(datetime.datetime.today()-datetime.timedelta(days=ultimos_dias),datetime.datetime.today())).order_by('-id')

		else:
			if len(filtros_json['agente_id']):
				bitacoras = bitacoras.filter(user__id=filtros_json['agente_id'])

			if len(filtros_json['fecha_inicio']) and len(filtros_json['fecha_final']):
				fecha_inicio_format = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')
				fecha_final_format = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
				bitacoras = bitacoras.filter(datetime__range=(fecha_inicio_format, fecha_final_format))

	else:
		#DEFAULT
		recientes = True
		bitacoras = bitacoras.filter(datetime__range=(datetime.datetime.today()-datetime.timedelta(days=ultimos_dias),datetime.datetime.today())).order_by('-id')

	return render_to_response('sections/bitacora/panel.html', locals())

@csrf_exempt
def search_bitacora(request):
	# agentes = Investigacion.objects.filter(candidato__estatus=True)
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		agente_id = request.POST.get('agente_id', '')
		fecha_inicio = request.POST.get('fecha_inicio', '')
		fecha_final = request.POST.get('fecha_final', '')
		request.session['filtros_search_bitacora'] = {'agente_id':agente_id, 'fecha_inicio':fecha_inicio,'fecha_final':fecha_final}
		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_bitacora'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')