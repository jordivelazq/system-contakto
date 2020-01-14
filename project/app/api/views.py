# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse
from app.compania.models import Compania, Contacto
from django.core import serializers
import json
from app.reportes.services import ServiceReporte
from app.util.email import EmailHandler

''' ----------------- EMPRESA -----------------'''

def empresa_get_contactos(request, empresa_id):
	data = serializers.serialize("json", Contacto.objects.filter(compania_id=empresa_id, status=True))
	return HttpResponse(data, mimetype='application/json')
