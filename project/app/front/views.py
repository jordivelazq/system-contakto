# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora

@login_required(login_url='/login', redirect_field_name=None)
def panel(request):
	user = request.user
	if user.groups.filter(name='contactos').count():
		return HttpResponseRedirect('/estatus')

	return HttpResponseRedirect('/candidatos/')

@login_required(login_url='/login', redirect_field_name=None)
def candidato(request):
	page = 'candidatos'
	return render_to_response('sections/candidato.html', locals())

@login_required(login_url='/login', redirect_field_name=None)
def clientes(request):
	page = 'clientes'
	return render_to_response('sections/clientes.html', locals())

@login_required(login_url='/login', redirect_field_name=None)
def reportes(request):
	page = 'reportes'
	return render_to_response('sections/reportes.html', locals())

@login_required(login_url='/login', redirect_field_name=None)
def bitacora(request):
	if not request.user.is_superuser:
		return HttpResponseRedirect('/panel')
	page = 'bitacora'
	bitacoras = Bitacora.objects.all().order_by('-id')[:50]
	return render_to_response('sections/bitacora.html', locals())	


def mint_login(request):
	state = ''
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active and user.is_staff:
				login(request, user)
				b = Bitacora(action='login', user=user)
				b.save()
				return HttpResponseRedirect('/candidatos')
			elif user.groups.filter(name='contactos').count():
				login(request, user)
				b = Bitacora(action='login', user=user)
				b.save()
				return HttpResponseRedirect('/estatus')
			else:
				state = "Tu cuenta no está activa, contacta a tu administrador"
		else:
			state = "Tu usuario y/o contraseña no son correctos"

	return render_to_response('sections/login.html', {'state': state}, context_instance=RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
def mint_logout(request):
	b = Bitacora(action='logout', user=request.user)
	b.save()
	logout(request)
	return HttpResponseRedirect('/login')
