# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.template import loader, Context
from django.template.loader import get_template
from django.contrib.auth.models import User

from app.investigacion.models import Investigacion
from app.compania.models import Contacto
from app.util.email import EmailHandler


class ServiceReporte:
	
	def getEstatusReporte(self, investigaciones):

		investigaciones = Investigacion.objects.filter(id__in=investigaciones)

		for i in investigaciones:
			i.ciudad = i.candidato.direccion_set.all()[0].ciudad
			i.estado = i.candidato.direccion_set.all()[0].estado
			i.entrevista = i.entrevistacita_set.all()[0] if i.entrevistacita_set.all().count() else None
			i.trayectoria = i.candidato.trayectorialaboral_set.filter(visible_en_status=True, status=True)

		return investigaciones

	def printReporte(self, data):
		htmly = get_template('sections/reportes/emailtemplate.html')
		d = { 'investigaciones': data }
		html_content = htmly.render(d)
		return html_content

	def getDestinatarios(self, request, contactos_id):
		destinatarios = []
		contactos_email = Contacto.objects.filter(id__in=contactos_id) if contactos_id else ''
		
		#Agregar email de contacto
		if len(contactos_email):
			for contacto in contactos_email:
				destinatarios.append(contacto.email)

		#Si no es sesión de admin, agregar el email del agente en sesión.
		if not request.user.is_superuser:
			agente_email = request.user.email
			destinatarios.append(agente_email)

		destinatarios.append('estudios@contakto.mx')

		return destinatarios
	
	def send_reporte_by_email(self, investigaciones, destinatarios):
		if len(investigaciones) == 0 or len(destinatarios) == 0:
			return False
		
		dest_list = destinatarios.split(',')
		sender_email = 'estatus.contakto@gmail.com'

		reporte = self.getEstatusReporte(investigaciones)
		html_content = self.printReporte(reporte)

		data = {
			'subject': 'Estatus de Investigaciones',
			'from_email': sender_email,
			'to': dest_list,
			'text_content': '',
			'html_content': html_content
		}

		eh = EmailHandler()
		return eh.sendEmail(data)
