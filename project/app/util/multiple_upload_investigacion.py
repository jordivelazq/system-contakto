import xlrd
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User

from app.entrevista.models import EntrevistaFile
from app.investigacion.models import Investigacion
from app.persona.models import Persona, Direccion, Telefono
from app.compania.models import Contacto
from app.entrevista.models import EntrevistaCita
from app.cobranza.models import Cobranza
from app.agente.views import is_email_valid

init_row = 5

def multiple_upload(file_id, sheet_index, request_user):
		workbook, worksheet = read_file(file_id, sheet_index)

		if workbook and worksheet:
			items = get_items(worksheet, workbook)
			return save_items(items, request_user)

		return [{
			"msg": "Hubo problemas leyendo el archivo.",
			"type": "danger"
		}]

def get_items(worksheet, workbook):
	row_index = init_row
	limit = 100
	items = []

	while row_index < worksheet.nrows and row_index < limit:
		data = get_row(workbook, worksheet, row_index)
		items.append(data)
		row_index +=  1
	
	return items

def read_file(file_id, sheet_index):
	workbook = None
	worksheet = None

	try:
		file = EntrevistaFile.objects.get(id=file_id)
		workbook = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + str(file.record))
		worksheet = workbook.sheet_by_index(sheet_index)
	except Exception, e:
		print "read_file", e
		pass
		
	return (workbook, worksheet)

def get_fecha(workbook, worksheet, row_index, col_index, date_format = "%Y-%m-%d"):
	fecha = None

	if worksheet.cell_type(row_index, col_index) == 3:
		try:
			fecha = datetime(*xlrd.xldate_as_tuple(worksheet.cell_value(row_index, col_index), workbook.datemode)).date().strftime(date_format)
		except Exception, e:
			print "get_fecha", e
			pass
	
	if not fecha:
		try:
			fecha = datetime.strptime(worksheet.cell_value(row_index, col_index), "%d/%m/%Y").strftime(date_format)
		except Exception, e:
			print "get_fecha2", e
			pass
	
	return fecha

def get_hora(workbook, worksheet, row_index, col_index):
	hora = worksheet.cell_value(row_index, col_index)

	if worksheet.cell_type(row_index, col_index) == 3:
		try:
			hora = datetime.strptime(str(timedelta(days=hora)), '%H:%M:%S').strftime('%I:%M:%S %p')
		except Exception, e:
			print "get_hora", e
			pass
	
	return hora

def get_telefono(worksheet, row_index, col_index):
	value = worksheet.cell_value(row_index, col_index)
	if worksheet.cell_type(row_index, col_index) == 2:
		return str(int(value))

	return value

def get_row(workbook, worksheet, row_index):
	fecha_recibido = get_fecha(workbook, worksheet, row_index, 2)
	dia_cita = get_fecha(workbook, worksheet, row_index, 10, "%d/%m/%Y")
	hora_cita = get_hora(workbook, worksheet, row_index, 11)
	telefono = get_telefono(worksheet, row_index, 13)

	return {
		"ejecutivo": 				worksheet.cell_value(row_index, 0).strip().lower(),

		"contacto_correo": 	worksheet.cell_value(row_index, 1).strip().lower(),

		"fecha_recibido": 	fecha_recibido,
		"tipo_estudio": 		worksheet.cell_value(row_index, 3),
		"puesto": 					worksheet.cell_value(row_index, 6).strip(),
		"estatus": 					worksheet.cell_value(row_index, 8),

		"nombre": 					worksheet.cell_value(row_index, 4).strip(),
		"apellido": 				worksheet.cell_value(row_index, 5).strip(),
		"ciudad":						worksheet.cell_value(row_index, 7).strip(),

		"gestor": 					worksheet.cell_value(row_index, 9).strip(),
		"dia_cita": 				dia_cita,
		"hora_cita": 				hora_cita,

		"observaciones": 		worksheet.cell_value(row_index, 12).strip(),

		"telefono": 				telefono,
	}

def get_ejecutivo(email, request_user):
	ejecutivo = None
	if is_email_valid(email):
		if request_user.is_superuser:
			try:
				ejecutivo = User.objects.get(email=email)
			except Exception, e:
				print "get_ejecutivo", e
				pass
		else:
			ejecutivo = request_user
	
	return ejecutivo

def get_contacto(email):
	contacto = None
	if is_email_valid(email):
		try:
			contacto = Contacto.objects.get(email = email)
		except Exception, e:
			print "get_contacto", e
			pass

	return contacto

def save_persona(nombre, apellido):
	persona = Persona(
		nombre = nombre,
		apellido = apellido
	)

	try:
		persona.full_clean()
		persona.save()
	except Exception, e:
		print "save_persona", e
		pass

	return persona

def save_direccion(ciudad, persona):
	direccion = Direccion(
		persona = persona,
		ciudad = ciudad
	)

	try:
		direccion.full_clean()
		direccion.save()
	except Exception, e:
		print "save_direccion", e
		pass

def save_telefono(numero, persona):
	telefono = Telefono(
		persona = persona,
		numero = str(numero),
		categoria = 'movil'
	)

	try:
		telefono.full_clean()
		telefono.save()
	except Exception, e:
		print "save_telefono", e
		pass

def get_tipo_estudio(tipo_estudio):
	try:
		tipo_estudio = int(tipo_estudio)
	except Exception, e:
		print "get_tipo_estudio", e
		return None
	
	tipo_estudio = tipo_estudio if tipo_estudio in [1, 2] else None
	
	return tipo_estudio

def get_status(status):
	try:
		status = int(status)
	except Exception, e:
		print "get_status", e
		pass

	status = status if status in [0, 1, 2] else None

	return status - 1

def save_investigacion(ejecutivo, contacto, persona, puesto, fecha_recibido, tipo_estudio, status, observaciones):
	tipo_estudio = get_tipo_estudio(tipo_estudio)
	status = get_status(status)

	investigacion = Investigacion(
		agente = ejecutivo,
		candidato = persona,
		compania = contacto.compania,
		contacto = contacto,
		puesto = puesto,
		fecha_recibido = fecha_recibido,
		tipo_investigacion_status = tipo_estudio,
		status = status,
		tipo_investigacion_texto = observaciones
	)

	try:
		investigacion.full_clean()
		investigacion.save()
	except Exception, e:
		print "save_investigacion", e
		pass

	return investigacion

def save_entrevista(investigacion, gestor, dia_cita, hora_cita):
	autorizada = 1 if gestor and dia_cita and hora_cita else 0

	entrevista = EntrevistaCita(
		investigacion = investigacion,
		entrevistador = gestor,
		fecha_entrevista = dia_cita,
		hora_entrevista = hora_cita,
		autorizada = autorizada
	)

	try:
		entrevista.full_clean()
		entrevista.save()
	except Exception, e:
		print "save_entrevista", e
		pass

def save_cobranza(investigacion):
	Cobranza(investigacion = investigacion).save()

def save_items(items, request_user):
	response = []
	index = init_row
	for item in items:
		index += 1

		contacto = get_contacto(item["contacto_correo"])
		if not contacto:
			response.append({
				"msg": "Dato inv&aacute;lido para: contacto. Registro: " + str(index),
				"type": "danger"
			})
			continue

		ejecutivo = get_ejecutivo(item["ejecutivo"], request_user)
		if not ejecutivo:
			response.append({
				"msg": "Dato inv&aacute;lido para: ejecutivo. Registro: " + str(index),
				"type": "danger"
			})
			continue

		persona = save_persona(item["nombre"], item["apellido"])
		if not persona.id:
			response.append({
				"msg": "Dato inv&aacute;lido para: persona. Registro: +" + str(index),
				"type": "danger"
			})
			continue

		investigacion = save_investigacion(ejecutivo, contacto, persona, item["puesto"], item["fecha_recibido"], item["tipo_estudio"], item["estatus"], item["observaciones"])
		if not investigacion.id:
			response.append({
				"msg": "Dato inv&aacute;lido para: investigacion. Registro: " + str(index),
				"type": "danger"
			})
			continue

		save_direccion(item["ciudad"], persona)

		save_telefono(item["telefono"], persona)

		save_entrevista(investigacion, item["gestor"], item["dia_cita"], item["hora_cita"])
		
		save_cobranza(investigacion)

		response.append({
			"msg": "Investigaci&oacute;n creada: <a href='/candidato/investigacion/" + str(investigacion.id)  + "/editar'>" + str(investigacion.id)  + "</a>",
			"type": "success"
		})

	return response
