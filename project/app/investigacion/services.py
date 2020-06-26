# -*- coding: utf-8 -*-
from app.investigacion.models import Investigacion
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import pink, black, red, blue, green
from django.conf import settings
import datetime
import xlrd
import os
import re

from app.reportes.utils import TextUtility


class InvestigacionService:
	'''

	'''

	@staticmethod
	def getStatusList(investigacion):		
		status_list = {'investigacion': '', 'entrevista_resultado': '', 'entrevista_autorizada': ''}
		# NOTA: REVISAR ESTO PORQUE ESTA COMENTADO
		'''
		status_list['investigacion'] = investigacion.status
		status_list['entrevista_resultado'] = investigacion.entrevistapersona_set.all()[0].entrevistainvestigacion_set.all()[0].resultado if investigacion.entrevistapersona_set.all().count() else '0'
		status_list['entrevista_autorizada'] = investigacion.entrevistacita_set.all()[0].autorizada
		'''

		return status_list

	@staticmethod
	def clean_type(value):
		doc_list = (
					('servicios','SERVICIOS (LUZ, AGUA, TELÉFONO)'),
					('gastos_automovil','GASTOS AUTOMÓVIL'),
					('transporte_publico','TRANSPORTE PÚBLICO'),
					('alimentacion','ALIMENTACIÓN'),
					('educacion','EDUCACIÓN'),
					('medico','MÉDICO'),
					('serv_domestico','SERVICIO DOMÉSTICO'),
					('deuda1','DEUDA 1'),
					('deuda2','DEUDA 2'),
					('conyuge','CÓNYUGE'),
				)

		for d in doc_list:
			if d[0] == value:
				return d[1].decode('utf-8').replace('_', ' ')
		return str(value).replace('_', ' ')

	@staticmethod
	def clean_currency(value, currency=''):
		try:
			return '$ '+str(float(value))+' '+currency
		except Exception as e:
			return str(value.upper())


	'''-------------- Funciones auxiliares para reportes PDF -------------- '''
	@staticmethod
	def set_header_footer(c,tipo_reporte=''):
		#Header con logo Contakto
		logo_contakto = settings.MEDIA_ROOT+'/logo_black.jpg'
		header_text = 'ESTUDIO SOCIOECONÓMICO' if tipo_reporte == 'completo' else 'ESTUDIO LABORAL'
		c.translate(0.5*inch,0.5*inch)
		c.setFont("Helvetica-Bold", 18)
		c.drawString(-0.25*inch, 10.75*inch, header_text)
		c.setFont("Helvetica", 14)
		c.line(-0.25*inch, 10.5*inch,7.5*inch,10.5*inch)
		c.drawInlineImage(logo_contakto, 6*inch, 10.75*inch, width=100,height=22)
		#Footer
		footer_text = 'El presente formato es para uso exclusivo de Contakto Uno S.C.'
		c.line(-0.25*inch, -0.2*inch,7.5*inch,-0.2*inch)
		c.setFont("Helvetica-Oblique", 8)
		c.drawString(4.3*inch, -0.4*inch, footer_text)
		#### GRID FOR DEV ONLY ###
		# InvestigacionService.draw_grid(c) 

	@staticmethod
	def draw_grid(c):
		c.setStrokeColor(pink)
		c.setFillColor(pink)
		c.grid([0, inch, 2*inch, 3*inch, 4*inch, 5*inch, 6*inch , 7*inch , 8*inch], [0, inch, 2*inch, 3*inch, 4*inch, 5*inch, 6*inch , 7*inch , 8*inch, 9*inch , 10*inch ])
		for y in xrange(0,11):
			c.drawString( 0,y*inch,str(y)+'in')
			for x in xrange(0,8):
				c.drawString( x*inch, 10*inch,str(x)+'in')
		c.setStrokeColor(black)
		c.setFillColor(black)

	@staticmethod
	def add_anexo_page(c,file_name,title='ANEXO'):
		#Header con logo Contakto
		InvestigacionService.set_header_footer(c,'completo')
		c.setFont("Helvetica-Bold", 14)
		c.drawString(3*inch, 9.5*inch, title)
		c.drawInlineImage(settings.MEDIA_ROOT+'/'+file_name, 0.5*inch, 3.5*inch, width=480, height=360)
		c.showPage()

	@staticmethod
	def draw_resultados_block(c,start_x, start_y, resultado, firma):
		RESULTADO_OPCIONES = (
			('0', 10),
		    ('1', 0.3),
			('2', 0.5),
			('3', 0.7),
		)

		row_x = start_x*inch
		row_y = start_y*inch
		
		c.setFont("Helvetica-Bold", 14)
		c.drawString(row_x, row_y, 'RESULTADO')
		c.setFont("Helvetica-Bold", 12)
		c.drawString(row_x+0.4*inch, row_y-0.3*inch, 'VIABLE')
		c.drawString(row_x+0.4*inch, row_y-0.5*inch, 'NO VIABLE')
		c.drawString(row_x+0.4*inch, row_y-0.7*inch, 'CON RESERVAS')

		x_list = [row_x+0.05*inch, row_x+0.25*inch]
		y_list = [row_y-(0.15*inch), row_y-(0.35*inch), row_y-(0.55*inch), row_y-(0.75*inch)]
		c.grid( x_list, y_list)

		try:
			index = int(resultado)
		except Exception as e:
			index = 0
		
		c.drawString(row_x+0.1*inch, row_y-RESULTADO_OPCIONES[index][1]*inch, 'X')

		c.setFont("Helvetica", 10)
		firma_text = 'Firma: ' + firma['correo'] + '__' + firma['candidato_id'] + '__' + firma['fecha']


		text_utility = TextUtility(c)
		c.drawString( text_utility.align_right(firma_text), 0, firma_text)

	@staticmethod
	def draw_textarea(flag, c, start_y, row_height, content):
		lines_used = 0
		line = ''
		for x in xrange(0,len(content)):
			max_line_length = 100
			if content[x] == '\n' or len(line) > max_line_length:
				if content[x] == '\n':
					line = line[:-1]
				elif len(line) > max_line_length:
					line += content[x]

				row_y = start_y*inch
				c.drawString(-0.25*inch, row_y, line)
				line = ''
				start_y -= row_height
				lines_used += 1
				if flag == 'max_lines_used' and lines_used > 1:
					break
			else: 
				line += content[x]
		if len(line):
			row_y = start_y*inch
			c.drawString(-0.25*inch, row_y, line)
			start_y -= row_height
			lines_used += 1

		return lines_used

	@staticmethod
	def trans_date(date):
		month = date.month
		labels = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
		monthTrans = labels[int(month)]
		return "%s/%s/%s" % (date.strftime("%d"), monthTrans.upper(), date.year)
