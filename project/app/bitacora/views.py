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
	ultimos_dias = 1
	bitacoras = Bitacora.objects.all()

	#para SEARCH sidebar
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='admint').order_by('username')
	filtros_json = request.session.get('filtros_search_bitacora', None)

	if filtros_json != None:
		if len(filtros_json['agente_id']):
			bitacoras = bitacoras.filter(user__id=filtros_json['agente_id'])

		fecha_inicio = None
		fecha_final = None
		if len(filtros_json['fecha_inicio']):
			fecha_inicio = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')

		if len(filtros_json['fecha_final']):
			fecha_final = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
		
		if fecha_inicio and fecha_final:
			bitacoras = bitacoras.filter(datetime__gte=fecha_inicio, datetime__lte=fecha_final)
		elif fecha_inicio:
			bitacoras = bitacoras.filter(datetime__gte=fecha_inicio)
		elif fecha_final:
			bitacoras = bitacoras.filter(datetime__lte=fecha_final)

	else:
		bitacoras = Bitacora.objects.filter(datetime__range=(datetime.datetime.today() - datetime.timedelta(days=ultimos_dias), datetime.datetime.today()))
	
	bitacoras = bitacoras.order_by('-id')[:500]

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
