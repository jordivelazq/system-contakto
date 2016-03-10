# -*- coding: utf-8 -*-
from django import template
from django.template import Context, loader, RequestContext
from app.cobranza.models import Cobranza
from app.investigacion.models import Investigacion
from app.entrevista.models import EntrevistaInvestigacion, EntrevistaGradoEscolaridad
from app.persona.models import TrayectoriaLaboral
import logging, re, os

register = template.Library()
	
@register.filter(name = 'tipo_investigacion_status')
def tipo_investigacion_status(value):
	status = ''
	try:
		status = Investigacion.TIPO_INVESTIGACION_OPCIONES[int(value)-1][1]
	except Exception, e:
		print e
	return status if len(status) else '---'
	
@register.filter(name = 'investigacion_status')
def investigacion_status(value):
	status = ''
	try:
		status = Investigacion.STATUS_OPCIONES[int(value)][1]
	except Exception, e:
		print e
	return status if len(status) else '---'

@register.filter(name = 'investigacion_status_gral')
def investigacion_status_gral(value):
	status = ''
	try:
		status = Investigacion.STATUS_GRAL_OPCIONES[int(value)][1]
	except Exception, e:
		print e
	return status if len(status) else '---'
	
@register.filter(name = 'investigacion_resultado')
def investigacion_resultado(value):
	status = ''
	try:
		status = Investigacion.RESULTADO_OPCIONES[int(value)][1]
	except Exception, e:
		print e
	return status if len(status) else '---'
	
@register.filter(name = 'entrevista_grado_academico')
def entrevista_grado_academico(value):
	grados_list = EntrevistaGradoEscolaridad.GRADO_OPCIONES
	for g in grados_list:
		if g[0] == value:
			return g[1]
	return '---'

@register.filter(name = 'entrevista_status_autorizada')
def entrevista_status_autorizada(value):
	index = ''
	try:
		index = 'Sí' if int(value) == 1 else 'No'
	except Exception, e:
		print e
	return index

@register.filter(name = 'motivo_salida')
def motivo_salida(value):
	status = ''
	try:
		status = TrayectoriaLaboral.SALIDA_OPCIONES[int(value)][1]
	except Exception, e:
		print e
	return status if len(status) else '---'

@register.filter
def filename(value):
    """Get basename of full-path. Return error if file not found."""
    return os.path.basename(value)

@register.filter(name = 'clean_type')
def clean_type(value):
	doc_list = (
				('acta_nacimiento','ACTA DE NACIMIENTO'),
				('acta_matrimonio','ACTA DE MATRIMONIO'),
				('comprobante_domicilio','COMPROBANTE DE DOMICILIO'),
				('id_oficial','COMPROBANTE DE IDENTIFICACIÓN'),
				('comprobante_nss','COMPROBANTE DE NSS'),
				('curp','CURP'),
				('cartilla_smn','CARTILLA SMN'),
				('ultimo_grado_estudio','ÚLTIMO GRADO DE ESTUDIOS:'),
				('cartas_laborales','CARTAS LABORALES'),
				('motivos_falta_docs','EN CASO DE QUE NO, ESPECIFICAR DOCUMENTO Y RAZÓN POR QUE NO LA PRESENTO'),
				('orden','ORDEN'),
				('limpieza','LIMPIEZA'),
				('conservacion','CONSERVACIÓN'),
				('disponibilidad','DISPONIBILIDAD'),
				('puntualidad','PUNTUALIDAD'),
				('apariencia_fisica','APARIENCIA FÍSICA'),
				('colaboracion','COLABORACIÓN'),
				('actitud','ACTITUD'),
				('trabajo','Ha trabajado anteriormente en la empresa'),
				('familiar','Tiene algún familiar trabajando en la empresa'),
				('investigado','Investigado'), 
				('conyuge','Cónyuge'), 
				('padres','Padres'), 
				('hermanos','Hermanos'), 
				('otros','Otros'), 
				('total','Total'), 
				('impuestos','Impuestos'), 
				('vestimenta','Vestimenta'), 
				('gastos_automovil','Gastos automóvil'), 
				('transporte_publico','Transporte publico'), 
				('alimentacion','Alimentación'), 
				('educacion','Educación'), 
				('medico','Médico'), 
				('diversos','Diversos'), 
				('servicios','Servicios (Luz, Agua, Teléfono)'), 
				('serv_domestico','Serv. doméstico'), 
				('seguros','Seguros'), 
				('deuda1','Deuda 1'), 
				('deuda2','Deuda 2'), 
				('otros','Otros'), 
				('total','Total'),
			)

	for d in doc_list:
		if d[0] == value:
			return d[1]
	return value

