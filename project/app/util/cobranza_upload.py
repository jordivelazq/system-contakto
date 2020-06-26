# -*- coding: utf-8 -*-

import csv

from app.cobranza.models import Cobranza
from app.investigacion.models import Investigacion

init_row = 1

def cobranza_upload(file_path):
  items = get_items(file_path)
  save_items(items)


def get_items(file_path):
  index = 0
  limit = 1000
  items = []

  with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
      if index >= init_row:
        row = get_row(row)
        items.append(row)
      
      if index > limit:
        break
        
      index += 1

  return items


def get_row(data):
	return {
		"investigacion_id": 				data[0],

		"monto":                    data[7],
		"folio":                    data[8],

		"razon_social":             data[11],

		"obs_cobranza":             data[13],
		"tipo":                     data[14]
	}


def parse_float(value):
  try:
    return float(value)
  except Exception as e:
    print (e)
    return None


def parse_int(value):
  try:
    return int(value)
  except Exception as e:
    print (e)
    return None
  
def parse_string(value):
  if not value:
    return ""

  try:
    string_parsed = value.decode('cp1252').encode("utf-8").replace("€?", "É")
  except Exception as e:
    print (e)
    string_parsed = value.decode('utf-8','ignore').encode("utf-8")
  
  return string_parsed


def update_cobranza(investigacion_id, monto, folio):
  cobranza = Cobranza.objects.get(investigacion=investigacion_id)

  cobranza.monto = parse_float(monto)
  cobranza.folio = folio

  cobranza.save()


def update_compania(investigacion_id, razon_social):
  inv = Investigacion.objects.get(id=investigacion_id)
  
  inv.compania.razon_social = razon_social
  inv.compania.save()


def update_investigacion(investigacion_id, obs_cobranza, tipo):
  inv = Investigacion.objects.get(id=investigacion_id)

  if inv.sucursal:
    inv.sucursal.nombre = parse_string(obs_cobranza)
    inv.sucursal.save()

  tipo = parse_int(tipo)
  tipos_validos = [item[0] for item in Investigacion.TIPO_INVESTIGACION_OPCIONES]
  if tipo in tipos_validos:
    inv.tipo_investigacion_status = tipo

  inv.save()


def save_items(items):
  index = 1

  for item in items:
    index += 1
    investigacion_id = item['investigacion_id']

    if investigacion_id:
      update_cobranza(investigacion_id, item['monto'], item['folio'])
      update_compania(investigacion_id, item['razon_social'])
      update_investigacion(investigacion_id, item['obs_cobranza'], item["tipo"])
