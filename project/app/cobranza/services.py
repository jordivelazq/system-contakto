# -*- coding: utf-8 -*-

from app.cobranza.models import Cobranza
from app.front.templatetags.fe_extras import investigacion_resultado

def get_cobranza(filtros_json, limit = 200):
    cobranza = Cobranza.objects.filter(investigacion__status_active=True)

    if filtros_json != None:
      if 'status_id' in filtros_json and len(filtros_json['status_id']) and int(filtros_json['status_id']) > -1:
        cobranza = cobranza.filter(investigacion__status_general=filtros_json['status_id'])
      if 'compania_id' in filtros_json and len(filtros_json['compania_id']):
        cobranza = cobranza.filter(investigacion__compania__id=filtros_json['compania_id'])
      if 'contacto_id' in filtros_json and len(filtros_json['contacto_id']):
        cobranza = cobranza.filter(investigacion__contacto__id=filtros_json['contacto_id'])
      if 'factura_folio' in filtros_json and len(filtros_json['factura_folio']):
        if filtros_json['factura_folio'] == 'por-facturar':
          cobranza = cobranza.filter(folio='')
        else:
          cobranza = cobranza.filter(folio=filtros_json['factura_folio'])
      if 'agente_select' in filtros_json and len(filtros_json['agente_select']):
        cobranza = cobranza.filter(investigacion__agente__id=filtros_json['agente_select'])

    cobranza = cobranza.order_by('id')[:limit]

    for c in cobranza:
      c.ciudad = c.investigacion.candidato.direccion_set.all()[0].ciudad if  c.investigacion.candidato.direccion_set.all()[0].ciudad else ''
      c.obs_cobranza = c.investigacion.sucursal.nombre.replace(",", " -") if c.investigacion.sucursal and c.investigacion.sucursal.nombre else ''
    
    return cobranza

def get_cobranza_csv_row(cob):
  return [
			cob.investigacion.id,
			cob.investigacion.fecha_recibido,
			cob.investigacion.compania.nombre.encode('utf-8'),
			cob.investigacion.candidato.nombre.encode('utf-8'),
			cob.investigacion.candidato.apellido.encode('utf-8'),
			cob.investigacion.puesto.encode('utf-8'),
			cob.ciudad.encode('utf-8'),
			cob.monto,
			cob.folio,
			cob.investigacion.contacto.email,
			cob.investigacion.contacto.nombre.encode('utf-8'),
			cob.investigacion.compania.razon_social.encode('utf-8'),
			cob.investigacion.agente.email,
			cob.obs_cobranza.encode('utf-8'),
			cob.investigacion.tipo_investigacion_status,
			investigacion_resultado(cob.investigacion.resultado),
			cob.investigacion.fecha_entrega,
			cob.investigacion.tipo_investigacion_texto.encode('utf-8')
		]
  
