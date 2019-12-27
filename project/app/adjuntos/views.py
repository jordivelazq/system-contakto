# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from app.persona.models import *
from app.persona.services import PersonaService 
from app.persona.forms import *
from app.investigacion.models import * 
from app.investigacion.forms import *
from app.compania.models import  *
from app.compania.forms import *
from app.entrevista.forms import *
from app.entrevista.models import *
from app.entrevista.services import EntrevistaService
from app.cobranza.models import *
from app.adjuntos.models import Adjuntos
from app.adjuntos.forms import AdjuntosForm

from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import datetime
import xlrd
import os
import json
from django.db.models import Q

### USUARIO CONTACTO TIENE ACCESO
@login_required(login_url='/login', redirect_field_name=None)
def panel_adjuntos(request, investigacion_id):
	is_usuario_contacto = True if any("contactos" in s for s in request.user.groups.values_list('name',flat=True)) else False
	#Si es usuario contacto, verificar que la investigación le corresponda
	if is_usuario_contacto and not Investigacion.objects.filter(id=investigacion_id, contacto__email=request.user.email).count():
		return HttpResponseRedirect('/')

	es_chrome = 'Chrome' in request.META['HTTP_USER_AGENT'] #Fix por pixeles en Chrome (input-group-addon de bootstrap)

	page = 'candidatos'
	seccion = 'adjuntos'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(id=investigacion_id)
	status_list = PersonaService.get_status_list(investigacion_id)

	adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else None
	
	#para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='admint')
	status_select = Investigacion.STATUS_GRAL_OPCIONES
	filtros_json = request.session.get('filtros_search', None)
	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

	is_user_captura = request.user.groups.filter(name="captura").count()

	return render_to_response('sections/candidato/adjuntos.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
def editar_adjuntos(request, investigacion_id):
	if not request.user.is_staff and request.user.groups.filter(name="captura").count() == 0:
		return HttpResponseRedirect('/')
	es_chrome = 'Chrome' in request.META['HTTP_USER_AGENT'] #Fix por pixeles en Chrome (input-group-addon de bootstrap)
	
	page = 'candidatos'
	seccion = 'adjuntos'
	status = ''
	msg = ''
	investigacion = Investigacion.objects.get(id=investigacion_id)
	status_list = PersonaService.get_status_list(investigacion_id)
	adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else Adjuntos(investigacion=investigacion)

	#para SEARCH
	empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
	empresas_select_todas = Compania.objects.filter(status=True).order_by('nombre')
	agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(username='admint')
	status_select = Investigacion.STATUS_GRAL_OPCIONES
	filtros_json = request.session.get('filtros_search', None)

	datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

	if request.method == 'POST':
		adjuntos_form = AdjuntosForm(request.POST, request.FILES, instance=adjuntos)
		if adjuntos_form.is_valid():
			adjuntos_form.save()
			return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/adjuntos/')
	else:
		adjuntos_form = AdjuntosForm(instance=adjuntos)

	return render_to_response('sections/candidato/editar_adjuntos.html', locals(), context_instance=RequestContext(request))
