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


''' ----------------- REPORTE -----------------'''

def reporte_enviar_correo(request):
	sr = ServiceReporte()

	user = request.user

	data = {
		'status': False
	}
	filtros = request.session.get('filtros_search_reportes', None)
	if 'contacto_id' not in filtros or len(filtros['contacto_id']) == 0:
		return data
	else:
		try:
			dest_list = sr.getDestinatarios(request,filtros['contacto_id'])
			contacto = Contacto.objects.get(id=filtros['contacto_id'])
			user = request.user
			sender_email = 'estatus@contakto.mx'
		except:
			return data

	reporte = sr.getReporte(filtros)
	html_content = sr.printReporte(reporte)
	eh = EmailHandler()
	response = True
	response = eh.sendEmail({
		'subject': 'Status *' + filtros['compania_nombre'] + '*',
		'from_email': sender_email,
		'to': dest_list,
		'text_content': '',
		'html_content': html_content
	})

	# eh.sendEmail({
	# 	'subject': 'Status *' + filtros['compania_nombre'] + '*',
	# 	'from_email': sender_email,
	# 	'to': ['info@mintitmedia.com'],
	# 	'text_content': '',
	# 	'html_content': html_content
	# })

	data['status'] = response
	return HttpResponse(json.dumps(data), mimetype='application/json')
