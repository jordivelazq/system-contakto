# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse
from app.compania.models import Contacto
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

''' ----------------- EMPRESA -----------------'''

def empresa_get_contactos(request, empresa_id):
	data = serializers.serialize("json", Contacto.objects.filter(compania_id=empresa_id, status=True).order_by('nombre'))
	return HttpResponse(data, content_type='application/json')

@csrf_exempt
def add_investigacion(request):
	print(request.method)
	print(request.body)
	return JsonResponse({'status':'success'})
	