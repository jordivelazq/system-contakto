# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.bitacora.models import Bitacora
from app.persona.models import *
from app.investigacion.models import *
from app.persona.forms import * 
from app.investigacion.models import * 
from app.investigacion.forms import *
from app.investigacion.services import *
from django.forms.models import modelformset_factory
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import pink, black, red, blue, green
from django.conf import settings
from app.reportes.utils import TextUtility
import datetime
import xlrd
import os

inv_serv = InvestigacionService()

@csrf_exempt
def exportar_pdf(request, investigacion_id, tipo_reporte):
	investigacion = Investigacion.objects.get(pk=investigacion_id)
	candidato = investigacion.candidato
	telefonos = candidato.telefono_set.all()
	trayectoria = candidato.trayectorialaboral_set.filter(status=True, visible_en_status=True)
	domicilio = candidato.direccion_set.all()[0]
	origen = candidato.origen_set.all()[0]
	
	legalidad = candidato.legalidad_set.all()
	seguro = candidato.seguro_set.all()

	if tipo_reporte == 'completo':
		entrevista_persona = investigacion.entrevistapersona_set.all()[0]
		entrevista_inv = entrevista_persona.entrevistainvestigacion_set.all()[0]
		licencia = entrevista_persona.entrevistalicencia_set.all()[0]
		infonavit = entrevista_persona.entrevistaprestacionvivienda_set.filter(categoria_viv='infonavit')[0]
		fonacot = entrevista_persona.entrevistaprestacionvivienda_set.filter(categoria_viv='fonacot')[0]
		info_personal = entrevista_persona.entrevistainfopersonal_set.all()[0]
		historial_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='trabajo')[0]
		historial_familiar_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='familiar')[0]
		salud = entrevista_persona.entrevistasalud_set.all()[0]
		actividades_habitos = entrevista_persona.entrevistaactividadeshabitos_set.all()[0]
		#ADADEMICA
		info_academica = entrevista_persona.entrevistaacademica_set.all()[0]
		info_academica_grados = entrevista_persona.entrevistagradoescolaridad_set.all()
		info_academica_idioma = entrevista_persona.entrevistaotroidioma_set.all()[0]
		#VIVIENDA
		situacion_vivienda = entrevista_persona.entrevistasituacionvivienda_set.all()[0]
		propietario = entrevista_persona.entrevistapropietariovivienda_set.all()[0]
		caracteristicas_vivienda = entrevista_persona.entrevistacaractaristicasvivienda_set.all()[0]
		tipo_inmueble = entrevista_persona.entrevistatipoinmueble_set.all()[0]
		distribucion_dimensiones = entrevista_persona.entrevistadistribuciondimensiones_set.all()[0]
		#MARCO FAMILIAR
		marco_familiar = entrevista_persona.entrevistamiembromarcofamiliar_set.all()
		#ECONOMIA MENSUAL
		ingresos = entrevista_persona.entrevistaeconomica_set.filter(tipo='ingreso')
		egresos = entrevista_persona.entrevistaeconomica_set.filter(tipo='egreso')
		#SITUACION ECONOMICA
		tarjetas = entrevista_persona.entrevistatarjetacreditocomercial_set.all()
		cuentas_deb = entrevista_persona.entrevistacuentadebito_set.all()
		autos = entrevista_persona.entrevistaautomovil_set.all()
		bienesraices = entrevista_persona.entrevistabienesraices_set.all()
		seguros = entrevista_persona.entrevistaseguro_set.all()
		deudas = entrevista_persona.entrevistadeudaactual_set.all()
		#REFERENCIAS PERSONALES
		referencias_personales = entrevista_persona.entrevistareferencia_set.all() if entrevista_persona.entrevistareferencia_set.all().count() else None
		#CUADRO DE EVALUACIÓN
		documentos_evaluados = entrevista_persona.entrevistadocumentocotejado_set.all() if entrevista_persona.entrevistadocumentocotejado_set.all().count() else None
		aspectos_hogar = entrevista_persona.entrevistaaspectohogar_set.all()
		aspectos_candidato = entrevista_persona.entrevistaaspectocandidato_set.all()
		#ADJUNTOS ("Fotografias")
		adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else None

	logo_contakto = settings.MEDIA_ROOT+'/logo_black.jpg'

	response = HttpResponse(content_type='application/pdf')
	filename = 'ESC ' + str(candidato) if tipo_reporte == 'completo' else 'ESL ' + str(candidato)
	response['Content-Disposition'] = 'attachment; filename="'+str(filename)+'.pdf"'

	c = canvas.Canvas(response)
	text_utility = TextUtility(c)

	#Header con logo Contakto
	inv_serv.set_header_footer(c, tipo_reporte)

	c.setFont("Helvetica-Bold", 9)
	c.drawString(6*inch, 10*inch, 'FECHA:')
	c.setFont("Helvetica", 9)

	# fecha
	c.drawString(text_utility.align_right(InvestigacionService.trans_date(investigacion.fecha_recibido)), 10*inch, InvestigacionService.trans_date(investigacion.fecha_recibido))	

	# solicitante nombre comercial
	c.drawString(text_utility.align_right(investigacion.compania.nombre), 9.85*inch, unicode(investigacion.compania.nombre.upper() if investigacion.compania.nombre else '---'))	

	# solicitante nombre comercial
	c.drawString(text_utility.align_right(investigacion.compania.razon_social), 9.7*inch, unicode(investigacion.compania.razon_social.upper() if investigacion.compania.razon_social else '---'))	

	# quien envía (Entrevista> info personal> quien envía)
	c.drawString(text_utility.align_right(investigacion.contacto.nombre), 9.55*inch, unicode(investigacion.contacto.nombre.upper() if investigacion.contacto else '---'))	

	#Datos inv/candidato
	labels = [	
				'NOMBRE DEL CANDIDATO:',
				'EDAD:',
				'PUESTO:',
			]

	datos = [ 	
				unicode(investigacion.candidato.nombre.upper()  if investigacion.candidato.nombre else '---'),
				unicode(investigacion.candidato.edad  if investigacion.candidato.edad else '---'),
				unicode(investigacion.puesto.upper()  if investigacion.puesto else '---'),
			]


	page_start_height = 8.5 if tipo_reporte == 'completo' else 9

	if tipo_reporte == 'completo':
		if adjuntos:
			if adjuntos.adj2.name:
				c.drawInlineImage(settings.MEDIA_ROOT+'/'+adjuntos.adj2.name, 0*inch, 8.75*inch, width=90, height=120)

	textobject = c.beginText()
	textobject.setTextOrigin(-0.25*inch, page_start_height*inch)
	textobject.setFont("Helvetica-Bold", 10)

	for line in labels:
		textobject.textLine(line)
	c.drawText(textobject)

	textobject = c.beginText()
	textobject.setTextOrigin(1.75*inch, page_start_height*inch)
	textobject.setFont("Helvetica", 10)

	for line in datos:
		textobject.textLine(line)
	c.drawText(textobject)

	#Teléfonos
	tel_casa = telefonos.filter(categoria='casa')[0] if telefonos.filter(categoria='casa').count() else ''
	tel_movil = telefonos.filter(categoria='movil')[0] if telefonos.filter(categoria='movil').count() else ''
	tel_recado = telefonos.filter(categoria='recado')[0] if telefonos.filter(categoria='recado').count() else ''

	textobject = c.beginText()
	textobject.setTextOrigin(5.15*inch,(page_start_height-0.65)*inch)
	textobject.setFont("Helvetica-Bold", 10)
	textobject.textLine('TEL. CASA:')
	textobject.textLine('TEL. MÓVIL:')
	textobject.textLine('TEL. RECADOS:')
	c.drawText(textobject)

	textobject = c.beginText()
	textobject.setTextOrigin(6.25*inch,(page_start_height-0.65)*inch)
	textobject.setFont("Helvetica", 10)
	textobject.textLine(unicode(tel_casa))
	textobject.textLine(unicode(tel_movil))
	textobject.textLine(unicode(tel_recado))
	c.drawText(textobject)

	#Datos generales
	c.setFont("Helvetica-Bold", 14)
	c.drawString(2*inch, (page_start_height-1.4)*inch, 'DATOS GENERALES')

	start_y = page_start_height-1.65
	row_height = 0.2

	# start_y -= row_height
	row_y = start_y*inch

	###DOMICILIO
	c.setFont("Helvetica-Bold", 12)
	c.drawString(-0.25*inch, row_y, 'DOMICILIO')
	c.setFont("Helvetica-Bold", 9)

	start_y -= row_height
	row_y = start_y*inch
	c.drawString(-0.25*inch, row_y, 'CALLE / NUM EXT-INT:')
	c.drawString(1.5*inch, row_y, 'COLONIA O FRACCIONAMIENTO:')
	c.drawString(4*inch, row_y, 'CIUDAD:')
	c.drawString(5*inch, row_y, 'ESTADO:')
	c.drawString(6.25*inch, row_y, 'CÓDIGO POSTAL:')

	start_y -= row_height
	row_y = start_y*inch
	c.setFont("Helvetica", 9)
	c.drawString(-0.25*inch, row_y, unicode(domicilio.calle.upper()))
	c.drawString(1.5*inch, row_y, unicode(domicilio.colonia.upper()))
	c.drawString(4*inch, row_y, unicode(domicilio.ciudad.upper()))
	c.drawString(5*inch, row_y, unicode(domicilio.estado.upper()))
	c.drawString(6.25*inch, row_y, unicode(domicilio.cp.upper()))

	start_y -= row_height
	row_y = start_y*inch
	c.setFont("Helvetica-Bold", 9)
	c.drawString(-0.25*inch, row_y, 'LUGAR DE NACIMIENTO:')
	c.drawString(3*inch, row_y, 'NACIONALIDAD:')
	c.drawString(5*inch, row_y, 'FECHA DE NACIMIENTO:')

	start_y -= row_height
	row_y = start_y*inch
	c.setFont("Helvetica", 9)
	c.drawString(-0.25*inch, row_y, unicode(origen.lugar.upper()))
	c.drawString(3*inch, row_y, unicode(origen.nacionalidad.upper()))

	fecha_nacimiento = origen.fecha.strftime("%d/%b/%Y") if origen.fecha else ''
	c.drawString(5*inch, row_y, unicode(fecha_nacimiento))
	
	start_y -= row_height
	row_y = start_y*inch
	c.setFont("Helvetica-Bold", 9)
	c.drawString(-0.25*inch, row_y, 'CURP:')
	if tipo_reporte == 'completo':
		c.drawString(2*inch, row_y, 'RFC:')
		c.drawString(3.75*inch, row_y, 'FOLIO IFE:')
		c.drawString(5.5*inch, row_y, 'CARTILLA SMN:')
	else:
		c.drawString(2*inch, row_y, 'NSS:')

	start_y -= row_height
	row_y = start_y*inch
	c.setFont("Helvetica", 9)
	c.drawString(-0.25*inch, row_y, unicode(candidato.curp.upper()) if candidato.curp else '')
	if tipo_reporte == 'completo':
		c.drawString(2*inch, row_y, unicode(entrevista_persona.rfc.upper()) if entrevista_persona.rfc else '')
		c.drawString(3.75*inch, row_y, unicode(entrevista_persona.ife))
		c.drawString(5.5*inch, row_y, unicode(entrevista_persona.smn))
	else:
		c.drawString(2*inch, row_y, unicode(candidato.nss.upper()) if candidato.nss else '' )

	firma = {
		'correo': str(investigacion.agente.email),
		'candidato_id': str(candidato.id),
		'fecha': str(InvestigacionService.trans_date(investigacion.fecha_recibido))
	}

	if tipo_reporte =='compacto':
		start_y -= 3*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 14)
		c.drawString(1.5*inch, row_y, 'OBSERVACIONES SOBRE INVESTIGACIÓN')
		c.grid([-20, 540], [row_y-10, 110])

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		lines_used = inv_serv.draw_textarea('', c, start_y, row_height, unicode(investigacion.observaciones_generales.upper()) if investigacion.observaciones_generales else '---')
		
		inv_serv.draw_resultados_block(c,3,1.25,investigacion.resultado, firma)


	if tipo_reporte == 'completo':
		inv_serv.draw_resultados_block(c,2,10,investigacion.resultado, firma)	

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'TIPO LICENCIA:')
		c.drawString(2.5*inch, row_y, 'No. LICENCIA:')
		c.drawString(4.5*inch, row_y, 'No. DE PASAPORTE O VISA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(licencia.tipo.upper()))
		c.drawString(2.5*inch, row_y, unicode(licencia.numero))
		c.drawString(4.5*inch, row_y, unicode(entrevista_persona.pasaporte))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'NSS (IMSS):')
		c.drawString(2*inch, row_y, 'ESTADO CIVIL:')
		c.drawString(3.5*inch, row_y, 'FECHA DE MATRIMONIO:')
		c.drawString(5.5*inch, row_y, 'RELIGIÓN:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(candidato.nss))
		c.drawString(2*inch, row_y, unicode(entrevista_persona.estado_civil if entrevista_persona.estado_civil else '' ))
		c.drawString(3.5*inch, row_y, unicode(entrevista_persona.fecha_matrimonio.upper()))
		c.drawString(5.5*inch, row_y, unicode(entrevista_persona.religion.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'TIEMPO RADICANDO EN LA CIUDAD:')
		c.drawString(2.5*inch, row_y, 'MEDIO QUE UTILIZA PARA TRANSPORTARSE:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(entrevista_persona.tiempo_radicando.upper()))
		c.drawString(2.5*inch, row_y, unicode(entrevista_persona.medio_utilizado.upper()))

		
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'CRÉDITO INFONAVIT ACTIVO:')
		c.drawString(1.75*inch, row_y, 'No. CRÉDITO:')
		c.drawString(3*inch, row_y, 'FECHA EN QUE FUE TRAMITADO:')
		c.drawString(5.35*inch, row_y, 'PARA QUÉ SE UTILIZA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, infonavit.activo)
		c.drawString(1.75*inch, row_y, infonavit.numero_credito)
		c.drawString(3*inch, row_y, infonavit.fecha_tramite.upper() if infonavit.fecha_tramite else '')
		c.drawString(5.35*inch, row_y, unicode(infonavit.uso.upper()) )

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'CRÉDITO FONACOT ACTIVO:')
		c.drawString(1.75*inch, row_y, 'No. CRÉDITO:')
		c.drawString(3*inch, row_y, 'FECHA EN QUE FUE TRAMITADO:')
		c.drawString(5.35*inch, row_y, 'PARA QUÉ SE UTILIZA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, fonacot.activo)
		c.drawString(1.75*inch, row_y, fonacot.numero_credito)
		c.drawString(3*inch, row_y, fonacot.fecha_tramite.upper() if fonacot.fecha_tramite else '')
		c.drawString(5.35*inch, row_y, unicode(fonacot.uso.upper()) )

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'QUIENES SON DEPENDIENTES ECONÓMICOS:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode( entrevista_persona.dependientes_economicos.upper() if entrevista_persona.dependientes_economicos else '---' ))

		start_y -= 2*row_height
		row_y = start_y*inch
		
		#INFO PERSONAL
		c.setFont("Helvetica-Bold", 14)
		c.drawString(2*inch, row_y, 'INFORMACIÓN PERSONAL')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'OBJETIVO PERSONAL:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_personal.objetivo_personal.upper()))	

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'OBJETIVO EN LA EMPRESA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_personal.objetivo_en_empresa.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'HA TRABAJADO ANTERIORMENTE EN LA EMPRESA:')
		c.drawString(3.75*inch, row_y, 'TIENE ALGÚN FAMILIAR TRABAJANDO EN LA EMPRESA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(historial_en_empresa.tiene.upper()))
		c.drawString(3.75*inch, row_y, unicode(historial_familiar_en_empresa.tiene.upper()))

		####
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'PUESTO:')
		c.drawString(1.5*inch, row_y, 'PERIODO:')
		c.drawString(3.75*inch, row_y, 'PUESTO:')
		c.drawString(5.5*inch, row_y, 'NOMBRE:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(historial_en_empresa.puesto.upper()))
		c.drawString(1.5*inch, row_y, unicode(historial_en_empresa.periodo.upper()))
		c.drawString(3.75*inch, row_y, unicode(historial_familiar_en_empresa.puesto.upper()))
		c.drawString(5.5*inch, row_y, unicode(historial_familiar_en_empresa.nombre.upper()))


		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'CUALIDADES:')
		c.drawString(3.25*inch, row_y, 'DEFECTOS:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_personal.cualidades.upper()))
		c.drawString(3.25*inch, row_y, unicode(info_personal.defectos.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'TIPO DE TRABAJO QUE LE GUSTA DESARROLLAR:')
		c.drawString(3.25*inch, row_y, 'ANTECEDENTES PENALES Y/O FAMILIARES:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_personal.trabajo_que_desarrolla.upper()))
		c.drawString(3.25*inch, row_y, unicode(info_personal.antecedentes_penales.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'CUENTA CON ALGÚN TATUAJE O ARETE: (CUANTOS Y EN QUE PARTE DEL CUERPO):')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_personal.tatuajes.upper()))

	#Fin de pagina 1
	c.showPage()

	if tipo_reporte == 'completo':
		inv_serv.set_header_footer(c,tipo_reporte)

		#DATOS DE SALUD
		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, 10*inch, 'DATOS DE SALUD')

		start_y = 9.5
		row_height = 0.2

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'PESO (KG):')
		c.drawString(1*inch, row_y, 'ESTATURA (MTS):')
		c.drawString(2.5*inch, row_y, 'SALUD FÍSICA:')
		c.drawString(4*inch, row_y, 'SALUD VISUAL:')
		c.drawString(5.5*inch, row_y, 'EMBARAZADA (# MESES):')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(salud.peso_kg))
		c.drawString(1*inch, row_y, unicode(salud.estatura_mts))
		c.drawString(2.5*inch, row_y, unicode(salud.salud_fisica.upper()))
		c.drawString(4*inch, row_y, unicode(salud.salud_visual.upper()))
		c.drawString(5.5*inch, row_y, unicode(salud.embarazo_meses.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'EJERCICIO QUE PRACTICA Y CON QUE FRECUENCIA LO HACE:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(salud.ejercicio_tipo_frecuencia.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ACCIDENTES:')
		c.drawString(3.5*inch, row_y, 'INTERVENCIONES QUIRÚRGICAS:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(salud.accidentes.upper()))
		c.drawString(3.5*inch, row_y, unicode(salud.intervenciones_quirurgicas.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ENFERMEDADES QUE PADECEN FAMILIARES:')
		c.drawString(3.5*inch, row_y, 'HA ESTADO BAJO ALGÚN TRATAMIENTO MÉDICO O PSICOLÓGICO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(salud.enfermedades_familiares.upper()))
		c.drawString(3.5*inch, row_y, unicode(salud.tratamiento_medico_psicologico.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ENFERMEDADES PADECIDAS CON MAYOR FRECUENCIA:')
		c.drawString(3.5*inch, row_y, 'INSTITUCIÓN MÉDICA A LA QU ACUDE:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(salud.enfermedades_mayor_frecuencia.upper()))
		c.drawString(3.5*inch, row_y, unicode(salud.institucion_medica.upper()))


		#ACTIVIDADES Y HABITOS
		start_y -= 6*row_height
		row_y = start_y*inch

		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, row_y, 'ACTIVIDADES Y HÁBITOS')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'SU TIEMPO LIBRE LO DEDICA A:')
		c.drawString(5.5*inch, row_y, 'ACTIVIDADES EXTRAS:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(actividades_habitos.tiempo_libre.upper()))
		c.drawString(5.5*inch, row_y, unicode(actividades_habitos.extras.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ESPECIFICAR CUANTO TIEMPO CONSUME:')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(0*inch, row_y, 'TABACO:')
		c.drawString(2.5*inch, row_y, 'ALCOHOL:')
		c.drawString(5*inch, row_y, 'OTRAS:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(0*inch, row_y, unicode(actividades_habitos.frecuencia_tabaco.upper()))
		c.drawString(2.5*inch, row_y, unicode(actividades_habitos.frecuencia_alcohol.upper()))
		c.drawString(5*inch, row_y, unicode(actividades_habitos.frecuencia_otras_sust.upper()))

		#INFORMACION ACADEMICA
		start_y -= 6*row_height
		row_y = start_y*inch

		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, row_y, 'INFORMACIÓN ACADÉMICA')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ESCOLARIDAD')
		c.drawString(1.75*inch, row_y, 'INSTITUCIÓN')
		c.drawString(3.9*inch, row_y, 'LUGAR (CIUDAD)')
		c.drawString(5.5*inch, row_y, 'AÑOS')
		c.drawString(6.5*inch, row_y, 'CERTIFICADO')

		for grado in info_academica_grados:
			start_y -= row_height
			row_y = start_y*inch
			c.setFont("Helvetica-Bold", 9)
			c.drawString(-0.25*inch, row_y, unicode(grado.grado.upper().replace('_', ' ')))
			c.setFont("Helvetica", 9)
			c.drawString(1*inch, row_y, unicode(grado.institucion.upper()))
			c.drawString(3.75*inch, row_y, unicode(grado.ciudad.upper()))
			c.drawString(5.25*inch, row_y, unicode(grado.anos.upper()))
			c.drawString(6.5*inch, row_y, unicode(grado.certificado.upper()))

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'DOMINIO DE OTRO IDIOMA:')
		c.drawString(2*inch, row_y, 'PORCENTAJE:')
		c.drawString(4*inch, row_y, 'CEDULA PROFESIONAL:')
		c.drawString(5.75*inch, row_y, 'AÑO DE EXPEDICIÓN:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_academica_idioma.idioma.upper()))
		c.drawString(2*inch, row_y, unicode(info_academica_idioma.porcentaje))
		c.drawString(4*inch, row_y, unicode(info_academica.cedula_profesional.upper()))
		c.drawString(5.75*inch, row_y, unicode(info_academica.cedula_prof_ano_exp))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ESTUDIA ACTUALMENTE (INSTITUCIÓN, QUÉ ESTUDIA, HORARIOS, DÍAS):')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(info_academica.estudios_actuales.upper()))

		#Grid para tabla Info. Académica
		start_y = 3.85
		row_y = start_y*inch
		x_list = [-0.3*inch, 0.9*inch, 3.65*inch, 5.15*inch, 6.35*inch, 7.5*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch), row_y-(0.6*inch), row_y-(0.8*inch), row_y-(1*inch), row_y-(1.2*inch), row_y-(1.4*inch) ]
		c.grid( x_list, y_list)

		#Fin de pagina 2
		c.showPage()

		#PAGINA 3
		inv_serv.set_header_footer(c,tipo_reporte)

		#SITUACION DE LA VIVIENDA
		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, 10*inch, 'SITUACIÓN DE LA VIVIENDA')

		start_y = 9.75
		row_height = 0.2

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'NOMBRE DEL PROPIETARIO:')
		c.drawString(3*inch, row_y, 'PARENTESCO:')
		c.drawString(5.5*inch, row_y, 'RENTA MENSUAL:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(propietario.nombre.upper()))
		c.drawString(3*inch, row_y, unicode(propietario.parentesco.upper()))
		c.drawString(5.5*inch, row_y, inv_serv.clean_currency(caracteristicas_vivienda.renta_mensual) if caracteristicas_vivienda.renta_mensual else '---')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(-0.25*inch, row_y, 'VIVIENDA')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0*inch, row_y, 'PROPIA:')
		c.drawString(1.5*inch, row_y, 'RENTADA:')
		c.drawString(2.75*inch, row_y, 'HIPOTECADA:')
		c.drawString(4*inch, row_y, 'PRESTADA:')
		c.drawString(5.25*inch, row_y, 'OTRA:')
		c.drawString(6*inch, row_y, 'VALOR APROXIMADO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(0*inch, row_y, unicode(caracteristicas_vivienda.propia.upper()))
		c.drawString(1.5*inch, row_y, unicode(caracteristicas_vivienda.rentada.upper()))
		c.drawString(2.75*inch, row_y, unicode(caracteristicas_vivienda.hipotecada.upper()))
		c.drawString(4*inch, row_y, unicode(caracteristicas_vivienda.prestada.upper()))
		c.drawString(5.25*inch, row_y, unicode(caracteristicas_vivienda.otra.upper()))
		c.drawString(6*inch, row_y, inv_serv.clean_currency(caracteristicas_vivienda.valor_aproximado) )

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(-0.25*inch, row_y, 'TIPO DE INMUEBLE')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0*inch, row_y, 'CASA:')
		c.drawString(1*inch, row_y, 'TERRENO COMPARTIDO:')
		c.drawString(2.75*inch, row_y, 'DEPARTAMENTO:')
		c.drawString(4.25*inch, row_y, 'VIVIENDA POPULAR:')
		c.drawString(6*inch, row_y, 'OTRO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(0*inch, row_y, unicode(tipo_inmueble.casa.upper()))
		c.drawString(1*inch, row_y, unicode(tipo_inmueble.terreno_compartido.upper()))
		c.drawString(2.75*inch, row_y, unicode(tipo_inmueble.departamento.upper()))
		c.drawString(4.25*inch, row_y, unicode(tipo_inmueble.vivienda_popular.upper()))
		c.drawString(6*inch, row_y, unicode(tipo_inmueble.otro_tipo.upper()))

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(-0.25*inch, row_y, 'DISTRIBUCIÓN DIMENSIONAL')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0*inch, row_y, 'HABITACIONES:')
		c.drawString(1.5*inch, row_y, 'BAÑOS:')
		c.drawString(2.5*inch, row_y, 'SALAS:')
		c.drawString(3.5*inch, row_y, 'COMEDOR:')
		c.drawString(4.75*inch, row_y, 'COCINA:')
		c.drawString(5.75*inch, row_y, 'PATIO:')
		c.drawString(6.75*inch, row_y, 'COCHERA:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(0*inch, row_y, unicode(distribucion_dimensiones.habitaciones.upper()))
		c.drawString(1.5*inch, row_y, unicode(distribucion_dimensiones.banos.upper()))
		c.drawString(2.5*inch, row_y, unicode(distribucion_dimensiones.salas.upper()))
		c.drawString(3.5*inch, row_y, unicode(distribucion_dimensiones.comedor.upper()))
		c.drawString(4.75*inch, row_y, unicode(distribucion_dimensiones.cocina.upper()))
		c.drawString(5.75*inch, row_y, unicode(distribucion_dimensiones.patios.upper()))
		c.drawString(6.75*inch, row_y, unicode(distribucion_dimensiones.cocheras.upper()))

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'TIEMPO DE RADICAR EN EL DOMICILIO:')
		c.drawString(3*inch, row_y, 'TIPO DE MOBILIARIO:')
		c.drawString(5.5*inch, row_y, 'SECTOR SOCIOECONÓMICO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(situacion_vivienda.tiempo_radicando.upper()))
		c.drawString(3*inch, row_y, unicode(situacion_vivienda.tipo_mobiliario.upper()))
		c.drawString(5.5*inch, row_y, unicode(situacion_vivienda.sector_socioeconomico.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'PERSONAS QUE VIVEN CON EL EVALUADO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(situacion_vivienda.personas_viven_con_evaluado.upper()))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'CONSERVACIÓN DE VIVIENDA:')
		c.drawString(4*inch, row_y, 'TAMAÑO APROXIMADO (MTS2):')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(situacion_vivienda.conservacion.upper()))
		c.drawString(4*inch, row_y, unicode(situacion_vivienda.tamano_aprox_mts2.upper()))

		#MARCO FAMILIAR
		start_y -= 3*row_height
		row_y = start_y*inch

		c.setFont("Helvetica-Bold", 14)
		c.drawString(3*inch, row_y, 'MARCO FAMILIAR')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 7)
		c.drawString(0*inch, row_y, 'ESPECIFICAR PADRES, HERMANOS, PAREJA E HIJOS, INCLUIR PERSONAS QUE RADIQUEN EN EL MISMO DOMICILIO AUNQUE NO SEAN FAMILIA NUCLEAR')


		start_y -= 2*row_height
		row_y = start_y*inch
		
		fam_qty = 0
		for familiar in marco_familiar:
			if familiar.nombre or familiar.edad or familiar.ocupacion or familiar.empresa or familiar.residencia:
				fam_qty = fam_qty + 1
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 8)
				c.drawString(-0.15*inch, row_y, unicode(familiar.tipo.upper()))
				c.drawString(0.75*inch, row_y, unicode(familiar.nombre.upper()))
				c.drawString(2.6*inch, row_y, unicode(familiar.edad.upper()))
				c.drawString(3.1*inch, row_y, unicode(familiar.ocupacion.upper()))
				c.drawString(4.9*inch, row_y, unicode(familiar.empresa.upper()))
				c.drawString(5.7*inch, row_y, unicode(familiar.residencia.upper()))
				c.drawString(6.6*inch, row_y, unicode(familiar.telefono.upper()))

		if fam_qty: #Imprimir tabla (headers y grid) solo si hay familiares
			start_y += fam_qty*row_height
			row_y = start_y*inch
			c.setFont("Helvetica-Bold", 8)
			c.drawString(-0.15*inch, row_y, 'PARENTESCO')
			c.drawString(0.75*inch, row_y, 'NOMBRE COMPLETO')
			c.drawString(2.6*inch, row_y, 'EDAD')
			c.drawString(3.1*inch, row_y, 'OCUPACIÓN')
			c.drawString(4.9*inch, row_y, 'EMPRESA')
			c.drawString(5.7*inch, row_y, 'RESIDENCIA')
			c.drawString(6.6*inch, row_y, 'TELÉFONO')
			x_list = [-0.25*inch, 0.65*inch, 2.5*inch, 3*inch, 4.8*inch, 5.6*inch , 6.5*inch , 7.65*inch]
			y_list = [ 1.5*inch, 1.7*inch, 1.9*inch, 2.1*inch, 2.3*inch, 2.5*inch, 2.7*inch , 2.9*inch , 3.1*inch, 3.3*inch , 3.5*inch, 3.7*inch, 3.9*inch, 4.1*inch, 4.3*inch, 4.5*inch]
			c.grid( x_list, y_list[(14-fam_qty):])

		else:
			start_y += fam_qty*row_height
			row_y = start_y*inch
			c.setFont("Helvetica-Bold", 9)
			c.drawString(3.1*inch, row_y, '(SIN MARCO FAMILIAR)')

		#Fin de pagina 3
		c.showPage()


		#PAGINA 4
		inv_serv.set_header_footer(c,tipo_reporte)

		#INFORMACIÓN ECONÓMICA MENSUAL
		c.setFont("Helvetica-Bold", 14)
		c.drawString(2*inch, 10*inch, 'INFORMACIÓN ECONÓMICA MENSUAL')

		start_y = 9.75
		row_height = 0.2

		start_y -= row_height
		row_y = start_y*inch 

		c.setFont("Helvetica-Bold", 12)
		c.drawString(1.25*inch, row_y, 'INGRESOS')
		c.drawString(5*inch, row_y, 'EGRESOS')

		start_y += 1.8*row_height
		row_y = start_y*inch 
		x_list = [0*inch,  3*inch,  7.5*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch)]
		c.grid( x_list, y_list)
		start_y -= row_height
		row_y = start_y*inch
		x_list = [0*inch, 1.75*inch, 3*inch, 6.25*inch, 7.5*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch), row_y-(0.6*inch), row_y-(0.8*inch), row_y-(1*inch), row_y-(1.2*inch), row_y-(1.4*inch), row_y-(1.6*inch), row_y-(1.8*inch), row_y-(2*inch), row_y-(2.2*inch), row_y-(2.4*inch), row_y-(2.6*inch), row_y-(2.8*inch), row_y-(3*inch), row_y-(3.2*inch) ]
		c.grid( x_list, y_list)		

		start_y = 9.75
		start_y -= row_height
		for i in ingresos:
			start_y -= row_height
			row_y = start_y*inch if i.concepto != 'total' else 6.55*inch
			font = 'Helvetica-Bold' if i.concepto == 'total' else 'Helvetica'
			c.setFont(font, 9) 
			c.drawString(0.2*inch, row_y, unicode( inv_serv.clean_type(i.concepto).upper()) )
			c.drawString(1.95*inch, row_y, inv_serv.clean_currency(i.monto))

		start_y = 9.75
		start_y -= row_height
		for e in egresos:
			start_y -= row_height
			row_y = start_y*inch
			font = 'Helvetica-Bold' if e.concepto == 'total' else 'Helvetica'
			c.setFont(font, 9) 
			c.drawString(3.2*inch, row_y, unicode( inv_serv.clean_type(e.concepto).upper()) )
			c.drawString(6.45*inch, row_y, inv_serv.clean_currency(e.monto))

		#SITUACION ECONÓMICA
		c.setFont("Helvetica-Bold", 14)
		c.drawString(3*inch, 5.75*inch, 'SITUACIÓN ECONÓMICA')

		start_y = 5.85

		for x in xrange(0,5):
			row_y = start_y*inch	
			x_list = [0*inch, 7.5*inch]
			y_list = [row_y-(0.2*inch), row_y-(0.4*inch)]
			c.grid( x_list, y_list)
			start_y -= row_height
			row_y = start_y*inch
			x_list = [0*inch, 1.87*inch, 3.75*inch, 5.6*inch, 7.5*inch]
			y_list = [row_y-(0.2*inch), row_y-(0.4*inch), row_y-(0.6*inch), row_y-(0.8*inch) ]
			c.grid( x_list, y_list)
			start_y -= 3*row_height
		
		start_y = 5.7

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(2.25*inch, row_y, 'TARJETAS DE CRÉDITO Y/O COMERCIALES')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0.1*inch, row_y, 'INSTITUCIÓN')
		c.drawString(2*inch, row_y, 'LÍMITE DE CRÉDITO')
		c.drawString(3.85*inch, row_y, 'PAGO MÍNIMO')
		c.drawString(5.7*inch, row_y, 'SALDO ACTUAL')
		if tarjetas.count():
			c.setFont("Helvetica", 9)
			for t in tarjetas:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, unicode(t.institucion.upper()))
				c.drawString(2*inch, row_y, inv_serv.clean_currency(t.limite_credito) )
				c.drawString(3.85*inch, row_y, inv_serv.clean_currency(t.pago_minimo) )
				c.drawString(5.7*inch, row_y, inv_serv.clean_currency(t.saldo_actual) )
		else:
			start_y -= 2*row_height

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(3*inch, row_y, 'CUENTAS DE DÉBITO')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0.1*inch, row_y, 'INSTITUCIÓN')
		c.drawString(2*inch, row_y, 'SALDO MENSUAL')
		c.drawString(3.85*inch, row_y, 'ANTIGÜEDAD')
		c.drawString(5.7*inch, row_y, 'AHORRO')

		if cuentas_deb.count():
			c.setFont("Helvetica", 9)
			for cuenta in cuentas_deb:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, unicode(cuenta.institucion.upper()))
				c.drawString(2*inch, row_y, inv_serv.clean_currency(cuenta.saldo_mensual) )
				c.drawString(3.85*inch, row_y, unicode(cuenta.antiguedad.upper()))
				c.drawString(5.7*inch, row_y, inv_serv.clean_currency(cuenta.ahorro) )
		else:
			start_y -= 2*row_height

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(3.25*inch, row_y, 'AUTOMÓVILES')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0.1*inch, row_y, 'MARCA')
		c.drawString(2*inch, row_y, 'MODELO Y AÑO')
		c.drawString(3.85*inch, row_y, 'LIQUIDADO')
		c.drawString(5.7*inch, row_y, 'VALOR COMERCIAL (M.N.)')

		if autos.count():
			c.setFont("Helvetica", 9)
			for a in autos:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, unicode(a.marca.upper()))
				c.drawString(2*inch, row_y, unicode(a.modelo_ano.upper()))
				c.drawString(3.85*inch, row_y, inv_serv.clean_currency(a.liquidacion))
				c.drawString(5.7*inch, row_y, inv_serv.clean_currency(a.valor_comercial))
		else:
			start_y -= 2*row_height

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(3.25*inch, row_y, 'BIENES RAÍCES')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0.1*inch, row_y, 'TIPO DE INMUEBLE')
		c.setFont("Helvetica-Bold", 7)
		c.drawString(1.95*inch, row_y, 'UBICACIÓN (DIRECCIÓN COMPLETA)')
		c.setFont("Helvetica-Bold", 9)
		c.drawString(3.85*inch, row_y, 'LIQUIDADO')
		c.drawString(5.7*inch, row_y, 'VALOR COMERCIAL (M.N.)')

		if bienesraices.count():
			c.setFont("Helvetica", 9)
			for br in bienesraices:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, unicode(br.tipo_inmueble.upper()))
				c.setFont("Helvetica", 6)
				c.drawString(1.9*inch, row_y, unicode(br.ubicacion.upper()))
				c.setFont("Helvetica", 9)
				c.drawString(3.85*inch, row_y, inv_serv.clean_currency(br.liquidacion) )
				c.drawString(5.7*inch, row_y, inv_serv.clean_currency(br.valor_comercial) )
		else:
			start_y -= 2*row_height

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(3.35*inch, row_y, 'SEGUROS')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(0.1*inch, row_y, 'EMPRESA')
		c.drawString(1.95*inch, row_y, 'TIPO DE SEGURO')
		c.drawString(3.85*inch, row_y, 'FORMA DE PAGO')
		c.drawString(5.7*inch, row_y, 'VIGENCIA')

		if seguros.count():
			c.setFont("Helvetica", 9)
			for s in seguros:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, unicode(s.empresa.upper()))
				c.drawString(1.9*inch, row_y, unicode(s.tipo.upper()))
				c.drawString(3.85*inch, row_y, unicode(s.forma_pago.upper()))
				c.drawString(5.7*inch, row_y, unicode(s.vigencia.upper()))
		else:
			start_y -= 2*row_height

		row_y = start_y*inch	
		x_list = [0*inch, 7.5*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch)]
		c.grid( x_list, y_list)
		start_y -= row_height
		row_y = start_y*inch
		x_list = [0*inch, 1.25*inch, 2.5*inch, 3.75*inch, 5*inch, 6.25*inch, 7.5*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch), row_y-(0.6*inch), row_y-(0.8*inch) ]
		c.grid( x_list, y_list)

		start_y = 1.35
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 11)
		c.drawString(2.75*inch, row_y, 'DEUDAS ACTUALES')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 6)
		c.drawString(0.1*inch, row_y, 'FECHA DE OTORGAMIENTO')
		c.setFont("Helvetica-Bold", 8)
		c.drawString(1.35*inch, row_y, 'TIPO')
		c.drawString(2.6*inch, row_y, 'INSTITUCIÓN')
		c.drawString(3.85*inch, row_y, 'CANTIDAD TOTAL')
		c.drawString(5.1*inch, row_y, 'SALDO ACTUAL')
		c.drawString(6.35*inch, row_y, 'PAGO MENSUAL')
		c.setFont("Helvetica", 9)
		if deudas.count():
			for d in deudas:
				start_y -= row_height
				row_y = start_y*inch
				c.drawString(0.1*inch, row_y, d.fecha_otorgamiento.upper() if d.fecha_otorgamiento else '')
				c.drawString(1.35*inch, row_y, unicode(d.tipo))
				c.drawString(2.6*inch, row_y, unicode(d.institucion))
				c.drawString(3.85*inch, row_y,  inv_serv.clean_currency(d.cantidad_total))
				c.drawString(5.1*inch, row_y, inv_serv.clean_currency(d.saldo_actual))
				c.drawString(6.35*inch, row_y, inv_serv.clean_currency(d.pago_mensual))

		#Fin de pagina 4
		c.showPage()


	#REFERENCIAS PERSONALES
	# if tipo_reporte == 'completo':
		if referencias_personales:
			inv_serv.set_header_footer(c,tipo_reporte)
			c.setFont("Helvetica-Bold", 14)
			c.drawString(2.5*inch, 10*inch, 'REFERENCIAS PERSONALES')
			start_y = 9.5
			index = 1
			for r in referencias_personales:
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 12)
				c.drawString(-0.25*inch, row_y, 'REFERENCIA '+str(index))
				index += 1
				start_y -= 2*row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'NOMBRE:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.nombre.upper()))
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'DOMICILIO:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.domicilio.upper()))
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'TELÉFONO:')
				c.drawString(4.5*inch, row_y, 'TIEMPO DE CONOCERLO:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.telefono.upper()))
				c.drawString(4.5*inch, row_y, unicode(r.tiempo_conocido.upper()))
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'PARENTESCO:')
				c.drawString(4.5*inch, row_y, 'OCUPACIÓN:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.parentesco.upper()))
				c.drawString(4.5*inch, row_y, unicode(r.ocupacion.upper()))
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'EN QUE LUGARES CONOCE QUE HA LABORADO EL EVALUADO:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.lugares_labor_evaluado.upper()))
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, 'OPINIÓN SOBRE EL CANDIDATO:')
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica", 9)
				c.drawString(-0.25*inch, row_y, unicode(r.opinion.upper()))
				start_y -= 5*row_height
				row_y = start_y*inch

			#Fin de Referencias personales
			c.showPage()


	#REFERENCIAS LABORALES (TRAYECTORIA)
	for t in trayectoria:
		evaluacion = t.evaluacion_set.all()[0]
		empresa = t.compania
		opinion_jefe = evaluacion.opinion_set.filter(categoria='1')[0] if evaluacion.opinion_set.filter(categoria='1').count() else None 
		opinion_rh = evaluacion.opinion_set.filter(categoria='2')[0] if evaluacion.opinion_set.filter(categoria='2').count() else None 
		informantes = evaluacion.informante_set.all()

		#Header con logo Contakto
		inv_serv.set_header_footer(c,tipo_reporte)

		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, 10*inch, 'REFERENCIA LABORAL')

		start_y = 10

		start_y -= row_height
		row_y = start_y*inch
		
		#Datos de trayectoria
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'EMPRESA: ' + unicode( empresa.nombre.upper() ))
		c.drawString(4.5*inch, row_y, 'TELÉFONO:')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		if empresa.razon_social:
			c.drawString(-0.25*inch, row_y, unicode( empresa.razon_social.upper() ))
		c.drawString(4.5*inch, row_y, unicode(empresa.telefono))

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'GIRO:')
		c.drawString(4.5*inch, row_y, 'UBICACIÓN:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(empresa.role.upper()))
		c.drawString(4.5*inch, row_y, unicode(empresa.ciudad.upper())  if empresa.ciudad else '---')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'PUESTOS:')
		c.drawString(1.25*inch, row_y, 'INICIAL:')
		c.drawString(4.25*inch, row_y, 'FINAL:')
		c.setFont("Helvetica", 9)
		c.drawString(2*inch, row_y, unicode(t.puesto_inicial.upper()) if t.puesto_inicial else '---')
		c.drawString(5*inch, row_y, unicode(t.puesto_final.upper()) if t.puesto_final else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'SUELDO:')
		c.drawString(1.25*inch, row_y, 'INICIAL:')
		c.drawString(4.25*inch, row_y, 'FINAL:')
		c.setFont("Helvetica", 9)
		c.drawString(2*inch, row_y, inv_serv.clean_currency(t.sueldo_inicial) if t.sueldo_inicial else '---')
		c.drawString(5*inch, row_y, inv_serv.clean_currency(t.sueldo_final) if t.sueldo_final else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'FECHAS LABORADAS:')
		c.drawString(1.25*inch, row_y, 'INGRESO:')
		c.drawString(4.25*inch, row_y, 'EGRESO:')
		c.setFont("Helvetica", 9)
		c.drawString(2*inch, row_y, unicode(t.periodo_alta.upper()) if t.periodo_alta else '---')
		c.drawString(5*inch, row_y, unicode(t.periodo_baja.upper()) if t.periodo_baja else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'FUNCIONES Y/O RESPONSABILIDADES:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(t.funciones.upper()) if t.funciones else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'ESPECIFICAR SI CUMPLIÓ CON LOS OBJETIVOS DEL PUESTO:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(t.cumplio_objetivos.upper()) if t.cumplio_objetivos else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'JEFE INMEDIATO:')
		c.drawString(4*inch, row_y, 'PUESTO:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(t.jefe_inmediato.upper()) if t.jefe_inmediato else '---')
		c.drawString(4*inch, row_y, unicode(t.jefe_inmediato_puesto.upper()) if t.jefe_inmediato_puesto else '---')

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'NÚMERO DE PERSONAS A SU CARGO:')
		c.drawString(4*inch, row_y, 'MANEJO DE VALORES:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, unicode(t.no_personas_cargo.upper()) if t.no_personas_cargo else '---')
		c.drawString(4*inch, row_y, 'SÍ' if t.manejo_valores == 1 else 'NO' if t.manejo_valores else '---')
		
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'MOTIVO DE RETIRO:')
		c.drawString(4*inch, row_y, 'POSIBILIDADES DE RECONTRATACIÓN:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		c.drawString(-0.25*inch, row_y, t.getMotivoSalida() if t.motivo_salida else '---')
		c.drawString(4*inch, row_y, unicode(t.recontratable.upper()) if t.recontratable else '---')
		
		start_y -= row_height
		row_y = start_y*inch

		x_list = [-0.25*inch, 7*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch)]
		c.grid( x_list, y_list)
		start_y -= row_height
		row_y = start_y*inch
		x_list = [-0.25*inch, 2*inch, 3.25*inch, 4.5*inch, 5.75*inch, 7*inch]
		y_list = [row_y-(0.2*inch), row_y-(0.4*inch), row_y-(0.6*inch), row_y-(0.8*inch), row_y-(1*inch), row_y-(1.2*inch), row_y-(1.4*inch), row_y-(1.6*inch), row_y-(1.8*inch), row_y-(2*inch), row_y-(2.2*inch), row_y-(2.4*inch), row_y-(2.6*inch), row_y-(2.8*inch), row_y-(3*inch) ]
		c.grid( x_list, y_list)

		start_y = 5.65
		row_y = start_y*inch
		
		c.setFont("Helvetica-Bold", 9)
		c.drawString(3*inch, row_y, 'EVALUACIÓN')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(0.2*inch, row_y, 'ACTITUDES Y APTITUDES')
		c.drawString(2.25*inch, row_y, 'EXCELENTE')
		c.drawString(3.7*inch, row_y, 'BUENO')
		c.drawString(4.85*inch, row_y, 'REGULAR')
		c.drawString(6.2*inch, row_y, 'MALO')

		EVALUACION_OPCIONES = (
		    ('1', 2.6),
			('2', 3.8),
			('3', 5.1),
			('4', 6.3),
		)

		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'PRODUCTIVIDAD')
		if evaluacion.productividad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.productividad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'ADAPTABILIDAD')
		if evaluacion.adaptabilidad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.adaptabilidad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'MOTIVACIÓN')
		if evaluacion.motivacion:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.motivacion)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'PUNTUALIDAD')
		if evaluacion.puntualidad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.puntualidad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'ASISTENCIA')
		if evaluacion.asistencia:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.asistencia)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'DISPONIBILIDAD')
		if evaluacion.disponibilidad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.disponibilidad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'RESPONSABILIDAD')
		if evaluacion.responsabilidad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.responsabilidad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'RELACIÓN CON JEFE INMEDIATO')
		if evaluacion.relacion_jefe_inmediato:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.relacion_jefe_inmediato)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'RELACIÓN CON COMPAÑEROS')
		if evaluacion.relacion_companeros:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.relacion_companeros)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'COMPROMISO')
		if evaluacion.compromiso:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.compromiso)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'HONESTIDAD')
		if evaluacion.honestidad:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.honestidad)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'TOMA DE DECISIONES')
		if evaluacion.toma_decisiones:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.toma_decisiones)-1][1]*inch, row_y, 'X')
		start_y -= row_height
		row_y = start_y*inch
		c.drawString(-0.15*inch, row_y, 'SOLUCIÓN DE PROBLEMAS')
		if evaluacion.solucion_problemas:
			c.drawString(EVALUACION_OPCIONES[int(evaluacion.solucion_problemas)-1][1]*inch, row_y, 'X')
		

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'OPINIÓN DE RECURSOS HUMANOS:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		if opinion_rh:
			inv_serv.draw_textarea('max_lines_used', c=c, start_y=start_y, row_height=row_height,content=unicode(opinion_rh.opinion.upper()) if opinion_rh else '---')

		start_y -= row_height * 2
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'OPINIÓN DE JEFE INMEDIATO:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		if opinion_jefe:
			inv_serv.draw_textarea('max_lines_used', c=c, start_y=start_y, row_height=row_height,content=unicode(opinion_jefe.opinion.upper()) if opinion_jefe else '---')

		start_y -= row_height
		row_y = start_y*inch

		for x in xrange(0,2):
		# for i in informantes:
			start_y -= row_height
			row_y = start_y*inch
			c.setFont("Helvetica-Bold", 9)
			c.drawString(-0.25*inch, row_y, 'NOMBRE DE INFORMANTE '+str(x+1)+':')
			c.drawString(4*inch, row_y, 'PUESTO:')
			start_y -= row_height
			row_y = start_y*inch
			c.setFont("Helvetica", 9)
			if informantes:
				if x < len(informantes):
					c.drawString(-0.25*inch, row_y, unicode(informantes[x].nombre.upper()) if informantes[x].nombre else '---')
					c.drawString(4*inch, row_y, unicode(informantes[x].puesto.upper()) if informantes[x].puesto else '---')
			else:	
				c.drawString(-0.25*inch, row_y, '---')
				c.drawString(4*inch, row_y, '---')

		c.showPage()
	#FIN Referencias laborales

	if tipo_reporte == 'completo':
		#CUADRO DE EVALUACIÓN
		inv_serv.set_header_footer(c,tipo_reporte)
		c.setFont("Helvetica-Bold", 14)
		c.drawString(2.5*inch, 10*inch, 'CUADRO DE EVALUACIÓN')
		start_y = 9.85

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(-0.25*inch, row_y, 'DOCUMENTOS EVALUADOS:')
		doc_list = (
					('acta_nacimiento','ACTA DE NACIMIENTO:'),
					('acta_matrimonio','ACTA DE MATRIMONIO:'),
					('comprobante_domicilio','COMPROBANTE DE DOMICILIO:'),
					('id_oficial','COMPROBANTE DE IDENTIFICACIÓN:'),
					('comprobante_nss','COMPROBANTE DE NSS:'),
					('curp','CURP:'),
					('cartilla_smn','CARTILLA SMN:'),
					('ultimo_grado_estudio','ÚLTIMO GRADO DE ESTUDIOS:'),
					('cartas_laborales','CARTAS LABORALES:'),
				)

		start_y -= row_height
		row_y = start_y*inch
		for d in doc_list:
			doc = documentos_evaluados.filter(tipo=d[0])[0] if documentos_evaluados.filter(tipo=d[0]).count() else None
			if doc:
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(-0.25*inch, row_y, d[1])
				c.setFont("Helvetica", 9)
				c.drawString(2.25*inch, row_y, u'\u2714' if doc.estatus else u'---')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'EN CASO DE QUE NO, ESPECIFICAR DOCUMENTO')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(-0.25*inch, row_y, 'Y RAZÓN POR QUE NO LA PRESENTÓ:')
		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		doc = documentos_evaluados.filter(tipo='motivos_falta_docs')[0]
		c.drawString(-0.25*inch, row_y, unicode(doc.observaciones.upper()) if doc.observaciones else '---')

		start_y = 9.85

		start_y -= row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(4.5*inch, row_y, 'CALIFICACIÓN DE 1 A 100%')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(4.5*inch, row_y, 'ASPECTO DEL HOGAR')
		hogar_list = (
					('orden','ORDEN:'),
					('limpieza','LIMPIEZA:'),
					('conservacion','CONSERVACIÓN:'),
				)

		for h in hogar_list:
			aspecto = aspectos_hogar.filter(tipo=h[0])[0] if aspectos_hogar.filter(tipo=h[0]).count() else None
			if aspecto:
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(4.75*inch, row_y, h[1])
				c.setFont("Helvetica", 9)
				c.drawString(6.25*inch, row_y, unicode(aspecto.estatus.upper())+'%' if aspecto.estatus else '---')

		start_y -= 2*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 9)
		c.drawString(4.5*inch, row_y, 'PERSONAL')
		candidato_list = (
					('disponibilidad','DISPONIBILIDAD:'),
					('puntualidad','PUNTUALIDAD:'),
					('apariencia_fisica','APARIENCIA FÍSICA:'),
					('colaboracion','COLABORACIÓN'),
					('actitud','ACTITUD'),
				)

		for can in candidato_list:
			aspecto = aspectos_candidato.filter(tipo=can[0])[0] if aspectos_candidato.filter(tipo=can[0]).count() else None
			if aspecto:
				start_y -= row_height
				row_y = start_y*inch
				c.setFont("Helvetica-Bold", 9)
				c.drawString(4.75*inch, row_y, can[1])
				c.setFont("Helvetica", 9)
				c.drawString(6.25*inch, row_y, unicode(aspecto.estatus.upper())+'%' if aspecto.estatus else '---')


		start_y -= 4*row_height
		row_y = start_y*inch
		c.setFont("Helvetica-Bold", 12)
		c.drawString(3*inch, row_y, 'CONCLUSIONES:')
		c.grid([-20, 540], [row_y-10, 110])

		start_y -= row_height*1.3
		row_y = start_y*inch
		c.setFont("Helvetica", 9)
		lines_used = inv_serv.draw_textarea('', c=c, start_y=start_y, row_height=row_height,content=unicode(entrevista_inv.conclusiones.upper()) if entrevista_inv.conclusiones else '---')

		start_y -= (lines_used+1)*row_height
		row_y = start_y*inch
		lines_used = inv_serv.draw_textarea('', c=c, start_y=start_y, row_height=row_height,content=unicode(investigacion.observaciones_generales.upper()) if investigacion.observaciones_generales else '---')

		inv_serv.draw_resultados_block(c,3,1.25,investigacion.resultado, firma)


		c.showPage()

	#FOTOGRAFIAS
	if tipo_reporte == 'completo':

		if adjuntos:
			if adjuntos.adj2.name:
				inv_serv.add_anexo_page(c,adjuntos.adj2.name,'FOTO DE CANDIDATO')
			if adjuntos.adj3.name:
				inv_serv.add_anexo_page(c,adjuntos.adj3.name,'FOTO INTERIOR 1')
			if adjuntos.adj4.name:
				inv_serv.add_anexo_page(c,adjuntos.adj4.name,'FOTO INTERIOR 2')
			if adjuntos.adj5.name:
				inv_serv.add_anexo_page(c,adjuntos.adj5.name,'FOTO EXTERIOR')
			if adjuntos.adj13.name:
				inv_serv.add_anexo_page(c,adjuntos.adj13.name,'CROQUIS')
			if adjuntos.adj7.name:
				inv_serv.add_anexo_page(c,adjuntos.adj7.name,'ANEXO 1')
			if adjuntos.adj8.name:
				inv_serv.add_anexo_page(c,adjuntos.adj8.name,'ANEXO 2')
			if adjuntos.adj9.name:
				inv_serv.add_anexo_page(c,adjuntos.adj9.name,'ANEXO 3')
			if adjuntos.adj10.name:
				inv_serv.add_anexo_page(c,adjuntos.adj10.name,'ANEXO 4')
			if adjuntos.adj11.name:
				inv_serv.add_anexo_page(c,adjuntos.adj11.name,'ANEXO 5')
			if adjuntos.adj12.name:
				inv_serv.add_anexo_page(c,adjuntos.adj12.name,'ANEXO 6')

	c.save()
	return response

@csrf_exempt
def exportar_html(request, investigacion_id, tipo_reporte):
	return render_to_response('sections/reportes/compacto.html', locals(), context_instance=RequestContext(request))
