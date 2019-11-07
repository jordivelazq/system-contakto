# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.template import loader, Context
from django.template.loader import get_template
from django.contrib.auth.models import User

from app.investigacion.models import Investigacion
from app.compania.models import Contacto
from app.util.email import EmailHandler


class ServiceReporte:

	def getReporte(self, data):

		if data == None or not len(data['compania_id']):
			return False

		investigaciones = Investigacion.objects.filter(status_active=True, compania__id=data['compania_id']).order_by('fecha_recibido')

		if 'contacto_id' in data and len(data['contacto_id']):
			investigaciones = investigaciones.filter(contacto__id=data['contacto_id'])

		if len(data['status_id']):
			investigaciones = investigaciones.filter(status_general=data['status_id'])

		if len(data['fecha_inicio']) and len(data['fecha_final']):
			fecha_inicio_format = datetime.datetime.strptime(data['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')
			fecha_final_format = datetime.datetime.strptime(data['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
			investigaciones = investigaciones.filter(fecha_recibido__range=(fecha_inicio_format, fecha_final_format))

		for i in investigaciones:
			i.ciudad = i.candidato.direccion_set.all()[0].ciudad
			i.entrevista = i.entrevistapersona_set.all()[0].entrevistainvestigacion_set.all()[0] if i.entrevistapersona_set.all().count() else None
			i.trayectoria = i.candidato.trayectorialaboral_set.filter(visible_en_status=True, status=True)

		return investigaciones
	
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
		d = Context({ 'investigaciones': data })
		html_content = htmly.render(d)
		return html_content

	def getDestinatarios(self,request,contacto_id):
		destinatarios = []
		contacto_email = Contacto.objects.filter(id=contacto_id)[0].email if contacto_id else ''
		admin_email = User.objects.filter(is_superuser=True)[0].email
		
		#Agregar email de contacto
		if len(contacto_email):
			destinatarios.append(contacto_email)
		#Si no es sesión de admin, agregar el email del agente en sesión.
		if not request.user.is_superuser:
			agente_email = request.user.email
			destinatarios.append(agente_email)
		
		# se pidio agregar este email tambien
		destinatarios.append('estatus@contakto.mx')

		#Agregar email de admin (irene@contakto.mx)
		destinatarios.append(admin_email)

		return destinatarios
	
	def send_reporte_by_email(self, investigaciones, destinatarios, user):
		print "perro", destinatarios.split(','), len(destinatarios)
		if len(investigaciones) == 0 or len(destinatarios) == 0:
			return False
		
		dest_list = destinatarios.split(',')
		sender_email = user.email or 'estatus@contakto.mx'

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
