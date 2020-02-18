# -*- coding: utf-8 -*-

from app.cobranza.models import Cobranza

def get_cobranza(filtros_json):
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
    
    cobranza = cobranza.order_by('id')[:500]

    for c in cobranza:
      c.ciudad = c.investigacion.candidato.direccion_set.all()[0].ciudad if  c.investigacion.candidato.direccion_set.all()[0].ciudad else ''
      c.obs_cobranza = c.investigacion.sucursal.nombre.replace(",", " -") if c.investigacion.sucursal and c.investigacion.sucursal.nombre else ''
    
    return cobranza
