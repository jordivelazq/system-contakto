# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.decorators import csrf
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

def descargar_app(request):
	return HttpResponseRedirect('https://github.com/garciadiazjaime/app-contakto/releases/download/v1.2.5/app-contakto-Setup-1.2.5.exe')

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
			elif user.groups.filter(name='captura').count():
				login(request, user)
				b = Bitacora(action='login', user=user)
				b.save()
				return HttpResponseRedirect('/candidatos')
			else:
				state = "Tu cuenta no está activa, contacta a tu administrador"
		else:
			state = "Tu usuario y/o contraseña no son correctos"

	return render(request, 'sections/login.html', {'state': state}, RequestContext(request))

@login_required(login_url='/login', redirect_field_name=None)
def mint_logout(request):
	b = Bitacora(action='logout', user=request.user)
	b.save()
	logout(request)
	return HttpResponseRedirect('/login')
