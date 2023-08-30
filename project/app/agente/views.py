# -*- coding: utf-8 -*-

import re 
from django.shortcuts import HttpResponse, render
from django.template import RequestContext
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.bitacora.models import Bitacora
from app.compania.models import Compania
from app.investigacion.models import Investigacion
from app.agente.models import AgenteInfo
import json
import datetime

def is_email_valid(email):  
	regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
	if(re.search(regex,email)):  
		return True

	return False
		

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def panel(request):
	page = 'agentes'
	users = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com').order_by('username')

	#Temporal para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='info@mintitmedia.com').order_by('username')
	status_select = Investigacion.STATUS_GRAL_OPCIONES
	filtros_json = request.session.get('filtros_search_agente', None)
 	
	if filtros_json != None and len(filtros_json['agente_id']):
		agente_seleccionado = User.objects.get(pk=filtros_json['agente_id'])
		investigaciones = Investigacion.objects.filter(status_active=True).order_by('candidato__nombre').filter(agente__id=filtros_json['agente_id'])
		
		if len(filtros_json['compania_id']):
			investigaciones = investigaciones.filter(Q(compania__id=filtros_json['compania_id']))
		if len(filtros_json['status_id']):
			investigaciones = investigaciones.filter(Q(status_general=filtros_json['status_id']))
		if len(filtros_json['fecha_inicio']) and len(filtros_json['fecha_final']):
			fecha_inicio_format = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')
			fecha_final_format = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
			investigaciones = investigaciones.filter(fecha_recibido__range=(fecha_inicio_format, fecha_final_format))

	return render(request, 'sections/agente/panel.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def nuevo(request):
	page = 'agentes'
	title = 'Crear nuevo agente'
	msg_class = 'alert alert-danger'
	username = password = first_name = last_name = telefono = ''
	state = []
	user = ''
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		telefono = request.POST.get('telefono', '')
		if not is_email_valid(username) or password == '' or first_name == '' or last_name == '':
			state.append('Favor de llenar los campos marcados con rojo')
			required_fields = True
		else:
			is_username_taken = User.objects.filter(username=username).count()

			if not is_username_taken:
				user = User(username=username, first_name=first_name, last_name=last_name, email=username)
				user.set_password(password)
				user.is_staff = True
				user.save()
				AgenteInfo(agente=user, telefono=telefono).save()
				b = Bitacora(action='crear-agente: ' + str(user), user=request.user)
				b.save()
				return HttpResponseRedirect('/agentes/exito')
			else:
				user_exists = True
				state.append('Este usuario ya está registrado, utilizar otro.')
				
	return render(request, 'sections/agente/form.html', locals(), RequestContext(request))

'''
	this function is not longer required, this function is handled throw NG
'''
@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def editar(request, user_id):
	user = User.objects.get(id=user_id)
	
	if user.agenteinfo_set.all().count():
		agente_info = user.agenteinfo_set.all()[0]
	else:
		agente_info = AgenteInfo(agente=user, telefono='')
		agente_info.save()

	page = 'agentes'
	editar_agente = True
	state = []
	msg_class = 'alert alert-danger'
	url = '/agente/' + str(user.id) + '/editar'
	title = 'Editar agente: ' + str(user)
	username = user.username
	first_name = user.first_name
	last_name = user.last_name
	telefono = agente_info.telefono
	enable_delete_agente = True
	# este el usuario mint admin
	if user.username == 'admin':
		return HttpResponseRedirect('/agentes')
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		telefono = request.POST.get('telefono', '')
		if not is_email_valid(username) or first_name == '' or last_name == '':
			state.append('Favor de llenar los campos marcados con rojo')
			required_fields = True
		else:
			is_username_taken = User.objects.filter(username=username).exclude(id=user_id).count()

			if not is_username_taken:
				user.username = username
				user.email = username
				user.first_name = first_name
				user.last_name = last_name
				if len(password):
					user.set_password(password)
				user.save()
				agente_info.telefono = telefono
				agente_info.save()
				msg_class = 'alert alert-success'
				state = 'Usuario guardado exitósamente'
				b = Bitacora(action='editar-agente: ' + str(user), user=request.user)
				b.save()
				return HttpResponseRedirect('/agentes/exito')
			else:
				user_exists = True
				state.append('Este usuario ya está registrado, utilizar otro.')
			
	return render(request, 'sections/agente/form.html', locals(), RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def borrar(request, user_id):
	if not request.user.is_superuser:
		return HttpResponseRedirect('/panel')
	deletedDate = str(datetime.datetime.today())
	bits = deletedDate.split('.')
	user = User.objects.get(id=user_id)
	user.is_active = False
	user.save()
	b = Bitacora(action='borrar-agente: ' + str(user), user=request.user)
	b.save()
	return HttpResponseRedirect('/agentes/exito')


@csrf_exempt
def search_agentes(request):
	response = { 'status' : False}
	if request.method == 'POST' and request.is_ajax():
		
		compania_id = request.POST.get('compania_id', '')
		compania_nombre = request.POST.get('compania_nombre', '')
		agente_id = request.POST.get('agente_id', '')
		status_id = request.POST.get('status_id', '')
		fecha_inicio = request.POST.get('fecha_inicio', '')
		fecha_final = request.POST.get('fecha_final', '')
		
		data = {
			'compania_id':compania_id, 
			'compania_nombre':compania_nombre, 
			'agente_id':agente_id, 
			'status_id':status_id, 
			'fecha_inicio':fecha_inicio,
			'fecha_final':fecha_final
		}

		request.session['filtros_search_agente'] = data
		
		response = { 'status' : True}

	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def reset_filtros(request):
	request.session['filtros_search_agente'] = None
	response = { 'status' : True}
	return HttpResponse(json.dumps(response), content_type='application/json')
