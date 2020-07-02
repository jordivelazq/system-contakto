# -*- coding: utf-8 -*-

from calendar import monthrange
import datetime
from django.db.models import Q
from django.db import connection

from app.cobranza.models import Cobranza
from app.front.templatetags.fe_extras import investigacion_resultado

def get_cobranza(filtros_json, limit = 200):
    cobranza = Cobranza.objects.values(
      'investigacion_id',
      'investigacion__fecha_recibido',
      'investigacion__compania__nombre',
      'investigacion__candidato__nombre',
      'investigacion__candidato__apellido',
      'investigacion__puesto',
      'monto',
      'folio',
      'investigacion__contacto__email',
      'investigacion__contacto__nombre',
      'investigacion__compania__razon_social',
      'investigacion__agente__email',
      'investigacion__tipo_investigacion_status',
      'investigacion__resultado',
      'investigacion__fecha_entrega',
      'investigacion__tipo_investigacion_texto'
    ).filter(investigacion__status_active=True)

    if filtros_json != None:
      if 'status_id' in filtros_json and len(filtros_json['status_id']) and int(filtros_json['status_id']) > -1:
        if int(filtros_json['status_id']) == 3:
          cobranza = cobranza.filter(Q(investigacion__status_general=0)|Q(investigacion__status_general=1))
        elif int(filtros_json['status_id']) == 4:
          cobranza = cobranza.filter(Q(investigacion__status_general=2)|Q(investigacion__status_general=1))
        else:
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
      
      fecha_inicio = None
      fecha_final = None
      if 'fecha_inicio' in filtros_json and len(filtros_json['fecha_inicio']):
        fecha_inicio = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')

      if 'fecha_final' in filtros_json and len(filtros_json['fecha_final']):
        fecha_final = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
      
      if fecha_inicio and fecha_final:
        cobranza = cobranza.filter(investigacion__fecha_recibido__gte=fecha_inicio, investigacion__fecha_recibido__lte=fecha_final)
      elif fecha_inicio:
        cobranza = cobranza.filter(investigacion__fecha_recibido__gte=fecha_inicio)
      elif fecha_final:
        cobranza = cobranza.filter(investigacion__fecha_recibido__lte=fecha_final)

    total_cobranza = cobranza.count()
    cobranza = cobranza.order_by('id')[:limit]

    # for c in cobranza:
    #   c.ciudad = c.investigacion.candidato.direccion_set.all()[0].ciudad if  c.investigacion.candidato.direccion_set.all()[0].ciudad else ''
    #   c.obs_cobranza = c.investigacion.sucursal.nombre.replace(",", " -") if c.investigacion.sucursal and c.investigacion.sucursal.nombre else ''
    
    return cobranza, total_cobranza

def get_cobranza_csv_row(cob):
  if cob["investigacion_id"]:
    item = [
      cob["investigacion_id"],
      cob["investigacion__fecha_recibido"],
      cob["investigacion__compania__nombre"].encode('utf-8'),
      cob["investigacion__candidato__nombre"].encode('utf-8'),
      cob["investigacion__candidato__apellido"].encode('utf-8'),
      cob["investigacion__puesto"].encode('utf-8'),
      "", # cob.ciudad.encode('utf-8'),
      cob["monto"],
      cob["folio"],
      cob["investigacion__contacto__email"],
      cob["investigacion__contacto__nombre"].encode('utf-8'),
      cob["investigacion__compania__razon_social"].encode('utf-8'),
      cob["investigacion__agente__email"],
      "", # cob.obs_cobranza.encode('utf-8'),
      cob["investigacion__tipo_investigacion_status"],
      investigacion_resultado(cob["investigacion__resultado"]),
      cob["investigacion__fecha_entrega"],
      cob["investigacion__tipo_investigacion_texto"].encode('utf-8')
    ]
    return item
  return ["ERROR", str(cob)]

def get_cobranza_csv_row_2(cob):
  item = [
    cob[0],
    cob[1],
    cob[2],
    cob[3],
    cob[4],
    cob[5],
    cob[6],
    cob[7],
    cob[8],
    cob[9],
    cob[10],
    cob[11],
    cob[12],
    cob[13],
    cob[14],
    cob[15],
    cob[16],
    cob[17]
  ]
  return item

def get_investigaciones_query(count, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio):
  values = [start_date, end_date]
  query = '''
    SELECT
  '''

  if count:
    query += '''
      count(*)
    '''
  else:
    query += '''
      i.id as '0',
      i.fecha_recibido as '1',
      cc.nombre as '2',
      pp.nombre as '3',
      pp.apellido as '4',
      i.puesto as '5',
      pd.estado as '6',
      cf.total as '7',
      cf.folio as '8',
      contacto.email as '9',
      contacto.nombre as '10',
      cc.razon_social as '11',
      user.email as '12',
      '' as observaciones,
      i.tipo_investigacion_status as '14',
      i.resultado as '15',
      i.fecha_entrega as '16',
      i.tipo_investigacion_texto as '17',
      i.status_general as '18'
      '''

  query += '''
    FROM investigacion_investigacion i
      INNER JOIN compania_compania cc ON cc.id = i.compania_id
      INNER JOIN persona_persona pp ON pp.id = i.candidato_id
      INNER JOIN compania_contacto contacto ON contacto.id = i.contacto_id
      INNER JOIN auth_user user ON user.id = i.agente_id
      LEFT JOIN cobranza_factura_investigacion cfi ON cfi.investigacion_id = i.id
      LEFT JOIN cobranza_factura cf ON cf.id = cfi.factura_id
      INNER JOIN persona_direccion pd ON pd.persona_id = pp.id
    WHERE i.fecha_recibido between %s AND %s
      AND i.status_active = 1
    '''

  if compania_id:
    query += '''
      AND i.compania_id = %s
      '''
    values.append(compania_id)
  
  if contacto_id:
    query += '''
      AND contacto.id = %s
      '''
    values.append(contacto_id)
  
  if agente_id:
    query += '''
      AND user.id = %s
    '''
    values.append(agente_id)
  
  if factura_filter == 'SIN_FACTURA':
    query += '''
      AND cf.folio IS NULL
    '''
  elif factura_filter == 'CON_FACTURA':
    query += '''
      AND cf.folio IS NOT NULL
    '''
  
  if status == '3':
    query += '''
      AND (i.status_general = %s OR i.status_general = %s)
    '''
    values.append(0)
    values.append(1)
  elif status == '4':
    query += '''
      AND (i.status_general = %s OR i.status_general = %s)
    '''
    values.append(2)
    values.append(1)
  elif status:
    query += '''
      AND i.status_general = %s
    '''
    values.append(status)
  
  if folio:
    query += '''
      AND cf.folio = %s
      '''
    values.append(folio)

  if not count:
    query += '''
      ORDER BY i.fecha_recibido, cf.folio
      LIMIT 1000
      '''

  return (query, values)
  
def get_investigaciones(get_count, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio):
  with connection.cursor() as cursor:

    query, values = get_investigaciones_query(get_count, start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio)

    cursor.execute(query, values)

    if get_count:
      return cursor.fetchone()

    return cursor.fetchall()

def get_total_investigaciones_facturadas():
  with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(DISTINCT investigacion_id) AS total FROM cobranza_factura_investigacion')
    return cursor.fetchone()

def get_cobranza_filters(request, filtros_json):
  today = datetime.datetime.today()
  start_date = datetime.date.today().replace(day=1)
  end_date = datetime.date.today().replace(day=monthrange(today.year, today.month)[1])
  compania_id = None
  contacto_id = None
  agente_id = None
  factura_filter = None
  status = None
  folio = None

  if filtros_json:
    if 'fecha_inicio' in filtros_json and len(filtros_json['fecha_inicio']):
      start_date = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime('%Y-%m-%d')

    if 'fecha_final' in filtros_json and len(filtros_json['fecha_final']):
      end_date = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime('%Y-%m-%d')
    
    if 'compania_id' in filtros_json and len(filtros_json['compania_id']):
      compania_id = filtros_json['compania_id']
    
    if 'contacto_id' in filtros_json and len(filtros_json['contacto_id']):
      contacto_id = filtros_json['contacto_id']
    
    if 'agente_select' in filtros_json and len(filtros_json['agente_select']):
      agente_id = filtros_json['agente_select']
    
    if 'factura_folio' in filtros_json and len(filtros_json['factura_folio']):
      factura_filter = filtros_json['factura_folio']
    
    if 'status_id' in filtros_json and len(filtros_json['status_id']) and int(filtros_json['status_id']) > -1:
      status = filtros_json['status_id']
    
    if 'folio' in filtros_json and len(filtros_json['folio']):
      folio = filtros_json['folio']
  else:
    request.session['filtros_search_cobranza'] = {
      'fecha_inicio': start_date.strftime('%d/%m/%y'),
      'fecha_final': end_date.strftime('%d/%m/%y')
    }
    filtros_json = request.session.get('filtros_search_cobranza', None)

  return (start_date, end_date, compania_id, contacto_id, agente_id, factura_filter, status, folio)
