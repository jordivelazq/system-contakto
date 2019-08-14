# -*- coding: utf-8 -*-
# documentacion de libreria xlrd:
# https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966
from django.conf import settings
import os
import datetime
import xlrd
import codecs
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contakto.settings")

from app.entrevista.models import EntrevistaFile

class PreCandidato(object):
	'''
		Clase driver para realizar lectura de datos del archivo de excel
	'''
	workbook = ''
	worksheet = ''
	errors = []
	
	def leerArchivo(self, file_id, sheet_index):
		'''
		Cargar archivo de excel a través de un ID y una index de página
		'''
		try:
			f = EntrevistaFile.objects.filter(id=file_id)
			self.workbook = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + str(f[0].record))
			self.worksheet = self.workbook.sheet_by_index(sheet_index)
		except Exception, e:
			print "Exception leerArchivo", e
			self.errors.append('Archivo no encontrado o corrupto')
			return 0
		return 1

	def getData(self):
		'''
		Función principal para jalar información de los diferentes rubros del posible candidato
		'''
		data = {
			'candidato': {
				'datos_generales': self.getGral(),
				'info_personal': self.getInfoPersonal(),
				'datos_salud': self.getDatosSalud(),
				'actividades_habitos': self.getActividadesHabitos(),
				'info_academica' : self.getInfoAcademica(),
				'situacion_vivienda': self.getSituacionVivienda(),
				'marco_familiar': self.getMarcoFamiliar(),
				'info_economica_mensual': self.getInfoEconomicaMensual(),
				'situacion_economica': self.getSituacionEconomica(),
				'referencias': self.getReferencias(),
				'cuadro_evaluacion': self.getCuadroEvaluacion()
			},
			'investigacion': self.getInvestigacion()
		}
		return data

	def getInvestigacion(self):
		'''
			Función para extraer los datos propios del investigación del precandidato
		'''
		data = {}
		try:
			try:
				data['fecha'] =  self.get_cell_value(rowx=1, colx=32)
				data['fecha_hora'] = self.get_cell_value(rowx=1, colx=38)
			except Exception, e:
				self.errors.append('Fecha de investigación inválida')
			
			data['empresa'] = self.get_cell_value(rowx=3, colx=9)
			data['puesto'] = self.get_cell_value(rowx=5, colx=4)
			
			data['conclusiones'] = self.get_cell_value(rowx=230,colx=0)
			data['viable'] = self.get_cell_value(rowx=250,colx=8)
			data['no_viable'] = self.get_cell_value(rowx=250,colx=20)
			data['reservas'] = self.get_cell_value(rowx=250,colx=33)

		except Exception, e:
			self.errors.append('No se pudo extraer los datos de investigación, revisar formato.')

		return data

	def getGral(self):
		'''
			Función para extraer los datos gerales del precandidato
		'''
		data = {
			'telefono': {
				'recados': {},
			},
			'direccion': {},
			'origen': {},
			'licencia': {},
			'infonavit': {},
			'fonacot': {},
		}
		try:
			data['nombre'] = self.get_cell_value(rowx=4, colx=9)
			data['edad'] = self.get_cell_value(rowx=4, colx=35)
			data['email'] = self.get_cell_value(rowx=6, colx=35)
			
			data['telefono']['casa'] = self.get_cell_value(rowx=5, colx=25)
			data['telefono']['movil'] = self.get_cell_value(rowx=5, colx=35)
			data['telefono']['recados']['numero'] = self.get_cell_value(rowx=6, colx=25)
			data['telefono']['recados']['parentesco'] = self.get_cell_value(rowx=7, colx=25)
			data['direccion']['calle'] = self.get_cell_value(rowx=12, colx=0)
			data['direccion']['num'] = self.get_cell_value(rowx=12, colx=8)
			data['direccion']['colonia'] = self.get_cell_value(rowx=12, colx=10)
			data['direccion']['ciudad'] = self.get_cell_value(rowx=12, colx=21)
			data['direccion']['estado'] = self.get_cell_value(rowx=12, colx=29)
			data['direccion']['cp'] = self.get_cell_value(rowx=12, colx=37)

			data['origen']['lugar'] = self.get_cell_value(rowx=13, colx=7)
			data['origen']['fecha'] = self.get_cell_value(rowx=13, colx=22)
			data['origen']['nacionalidad'] = self.get_cell_value(rowx=13, colx=35)

			data['rfc'] = self.get_cell_value(rowx=14, colx=2)
			data['curp'] = self.get_cell_value(rowx=14, colx=12)
			data['ife'] = self.get_cell_value(rowx=14, colx=24)
			data['smn'] = self.get_cell_value(rowx=14, colx=36)

			data['licencia']['tipo'] = self.get_cell_value(rowx=15, colx=6)
			data['licencia']['numero'] = self.get_cell_value(rowx=15, colx=17)
			data['pasaporte'] = self.get_cell_value(rowx=15, colx=34)

			data['nss'] = self.get_cell_value(rowx=16, colx=4)
			data['estado_civil'] = self.get_cell_value(rowx=16, colx=15)
			data['fecha_matrimonio'] = self.get_cell_value(rowx=16, colx=29)
			data['religion'] = self.get_cell_value(rowx=38, colx=6)
			data['religion_tiempo'] = self.get_cell_value(rowx=38, colx=25)
			data['tiempo_radicando'] = self.get_cell_value(rowx=17, colx=11)
			data['medio_utilizado'] = self.get_cell_value(rowx=17, colx=31)
			data['referencia_vacante'] = self.get_cell_value(rowx=18, colx=9)
			data['tiempo_transporte'] = self.get_cell_value(rowx=18, colx=36)
			data['dependientes_economicos'] = self.get_cell_value(rowx=132, colx=8)

			data['infonavit']['activo'] = self.get_cell_value(rowx=130, colx=6)
			data['infonavit']['numero'] = self.get_cell_value(rowx=130, colx=12)
			data['infonavit']['fecha_tramite'] = self.get_cell_value(rowx=130, colx=29)
			data['infonavit']['motivo'] = self.get_cell_value(rowx=130, colx=21)
			data['infonavit']['uso'] = self.get_cell_value(rowx=130, colx=37)
			
			data['fonacot']['activo'] = self.get_cell_value(rowx=131, colx=7)
			data['fonacot']['numero'] = self.get_cell_value(rowx=131, colx=16)
			data['fonacot']['fecha_tramite'] = self.get_cell_value(rowx=131, colx=29)
			data['fonacot']['uso'] = self.get_cell_value(rowx=131, colx=37)
		except Exception, e:
			self.errors.append('No se pudo extraer los datos generales, revisar formato.')
		
		return data

	def getInfoPersonal(self):
		'''
			Función para extraer los datos personales del precandidato
		'''
		data = {
				'trabajo_anterior_en_empresa': {},
				'familiar_en_empresa': {}
			}
		try:
			data['trabajo_anterior_en_empresa']['tiene'] = self.get_cell_value(rowx=26, colx=9)
			data['trabajo_anterior_en_empresa']['periodo'] = self.get_cell_value(rowx=26, colx=16)
			data['trabajo_anterior_en_empresa']['motivo_salida'] = self.get_cell_value(rowx=26, colx=24)
			data['trabajo_anterior_en_empresa']['puesto'] = self.get_cell_value(rowx=26, colx=33)
			data['trabajo_anterior_en_empresa']['sucursal'] = self.get_cell_value(rowx=26, colx=39)

			data['familiar_en_empresa']['tiene'] = self.get_cell_value(rowx=27, colx=9)
			data['familiar_en_empresa']['nombre'] = self.get_cell_value(rowx=27, colx=16)
			data['familiar_en_empresa']['puesto'] = self.get_cell_value(rowx=27, colx=24)
			data['familiar_en_empresa']['sucursal'] = self.get_cell_value(rowx=27, colx=39)	
			data['familiar_en_empresa']['parentesco'] = self.get_cell_value(rowx=27, colx=33)

			data['antecedentes_penales'] = self.get_cell_value(rowx=29, colx=8)
			data['tatuajes'] = self.get_cell_value(rowx=30, colx=21)
		except Exception, e:
			self.errors.append('No se pudo extraer los datos personales, revisar formato.')

		return data

	def getDatosSalud(self):
		'''
			Función para extraer los datos referentes a saludo del precandidato
		'''
		data = {}
		try:
			data['peso_kg'] = self.get_cell_value(rowx=32,colx=4)
			data['estatura_mts'] = self.get_cell_value(rowx=32,colx=12)
			data['salud_fisica'] = self.get_cell_value(rowx=32,colx=20)
			data['salud_visual'] = self.get_cell_value(rowx=32,colx=29)
			data['embarazo_meses'] = self.get_cell_value(rowx=32,colx=39)
			data['ejercicio_tipo_frecuencia'] = self.get_cell_value(rowx=33,colx=17)
			data['accidentes'] = self.get_cell_value(rowx=34,colx=4)
			data['intervenciones_quirurgicas'] = self.get_cell_value(rowx=34,colx=28)
			data['enfermedades_familiares'] = self.get_cell_value(rowx=35,colx=13)
			data['tratamiento_medico_psicologico'] = self.get_cell_value(rowx=35,colx=38)
			data['enfermedades_mayor_frecuencia'] = self.get_cell_value(rowx=36,colx=16)
			data['institucion_medica'] = self.get_cell_value(rowx=36,colx=36)
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de salud, revisar formato.')

		return data

	def getActividadesHabitos(self):
		'''
			Función para extraer los datos referentes a actividades recreativas del precandidato
		'''
		data = {}
		try:
			data['inactividad_laboral'] = self.get_cell_value(rowx=39,colx=9)
			data['inactividad_laboral_actividad'] = self.get_cell_value(rowx=39,colx=29)
			data['negocios'] = self.get_cell_value(rowx=41,colx=12)
			data['negocios_actividad'] = self.get_cell_value(rowx=41,colx=29)
			data['frecuencia_tabaco'] = self.get_cell_value(rowx=40,colx=16)
			data['frecuencia_alcohol'] = self.get_cell_value(rowx=40,colx=24)
			data['frecuencia_otras_sust'] = self.get_cell_value(rowx=40,colx=35)
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de Actividades y Hábitos, revisar formato.')

		return data

	def getInfoAcademica(self):
		'''
			Función para extraer los datos académicos del precandidato
		'''
		data = {
				'primaria': {},
				'secundaria': {},
				'preparatoria': {},
				'profesional': {},
				'otro_grado': {},
				'otro_idioma': {}
			}
		try:
			data['primaria']['institucion'] = self.get_cell_value(rowx=45,colx=5)
			data['primaria']['ciudad'] = self.get_cell_value(rowx=45,colx=19)
			data['primaria']['anos'] = self.get_cell_value(rowx=45,colx=30)
			data['primaria']['certificado'] = self.get_cell_value(rowx=45,colx=35)

			data['secundaria']['institucion'] = self.get_cell_value(rowx=46,colx=5)
			data['secundaria']['ciudad'] = self.get_cell_value(rowx=46,colx=19)
			data['secundaria']['anos'] = self.get_cell_value(rowx=46,colx=30)
			data['secundaria']['certificado'] = self.get_cell_value(rowx=46,colx=35)

			data['preparatoria']['institucion'] = self.get_cell_value(rowx=47,colx=5)
			data['preparatoria']['ciudad'] = self.get_cell_value(rowx=47,colx=19)
			data['preparatoria']['anos'] = self.get_cell_value(rowx=47,colx=30)
			data['preparatoria']['certificado'] = self.get_cell_value(rowx=47,colx=35)

			data['profesional']['institucion'] = self.get_cell_value(rowx=49,colx=5)
			data['profesional']['ciudad'] = self.get_cell_value(rowx=48,colx=19)
			data['profesional']['anos'] = self.get_cell_value(rowx=48,colx=30)
			data['profesional']['certificado'] = self.get_cell_value(rowx=48,colx=35)

			data['otro_grado']['institucion'] = self.get_cell_value(rowx=50,colx=5)
			data['otro_grado']['ciudad'] = self.get_cell_value(rowx=50,colx=19)
			data['otro_grado']['anos'] = self.get_cell_value(rowx=50,colx=30)
			data['otro_grado']['certificado'] = self.get_cell_value(rowx=50,colx=35)

			data['otro_idioma']['idioma'] = self.get_cell_value(rowx=51,colx=7)
			data['otro_idioma']['hablado'] = self.get_percentage(rowx=51,colx=14)
			data['otro_idioma']['leido'] = self.get_percentage(rowx=51,colx=18)
			data['otro_idioma']['escuchado'] = self.get_percentage(rowx=51,colx=23)

			data['cedula_profesional'] = self.get_cell_value(rowx=51,colx=32)
			data['cedula_prof_ano_exp'] = self.get_cell_value(rowx=51,colx=40)
			data['estudios_institucion'] = self.get_cell_value(rowx=52,colx=9)
			data['estudios_que'] = self.get_cell_value(rowx=52,colx=21)
			data['estudios_horarios'] = self.get_cell_value(rowx=52,colx=30)
			data['estudios_dias'] = self.get_cell_value(rowx=52,colx=37)

		except Exception, e:
			self.errors.append('No se pudo extraer los datos académicos, revisar formato.')

		return data

	def getSituacionVivienda(self):
		'''
			Función para extraer los datos referentes a las condiciones de vivvienda
		'''
		data = {
					'propietario': {},
					'caracteristicas_vivienda': {},
					'tipo_inmueble': {},
					'distribucion_dimensiones': {}
				}
		try:
			data['propietario']['nombre'] = self.get_cell_value(rowx=56,colx=8)
			data['propietario']['parentesco'] = self.get_cell_value(rowx=56,colx=24)

			data['caracteristicas_vivienda']['propia'] = self.get_cell_value(rowx=57,colx=6)
			data['caracteristicas_vivienda']['rentada'] = self.get_cell_value(rowx=57,colx=10)
			data['caracteristicas_vivienda']['hipotecada'] = self.get_cell_value(rowx=57,colx=16)
			data['caracteristicas_vivienda']['prestada'] = self.get_cell_value(rowx=57,colx=21)
			data['caracteristicas_vivienda']['otra'] = self.get_cell_value(rowx=57,colx=26)
			data['caracteristicas_vivienda']['valor_aproximado'] = self.get_cell_value(rowx=57,colx=35)
			data['caracteristicas_vivienda']['renta_mensual'] = self.get_cell_value(rowx=56,colx=37)

			data['tipo_inmueble']['casa'] = self.get_cell_value(rowx=58,colx=9)
			data['tipo_inmueble']['terreno_compartido'] = self.get_cell_value(rowx=58,colx=18)
			data['tipo_inmueble']['departamento'] = self.get_cell_value(rowx=58,colx=24)
			data['tipo_inmueble']['vivienda_popular'] = self.get_cell_value(rowx=58,colx=32)
			data['tipo_inmueble']['otro_tipo'] = self.get_cell_value(rowx=58,colx=36)

			data['distribucion_dimensiones']['habitaciones'] = self.get_cell_value(rowx=59,colx=14)
			data['distribucion_dimensiones']['banos'] = self.get_cell_value(rowx=59,colx=18)
			data['distribucion_dimensiones']['salas'] = self.get_cell_value(rowx=59,colx=22)
			data['distribucion_dimensiones']['comedor'] = self.get_cell_value(rowx=59,colx=27)
			data['distribucion_dimensiones']['cocina'] = self.get_cell_value(rowx=59,colx=32)
			data['distribucion_dimensiones']['patios'] = self.get_cell_value(rowx=59,colx=36)
			data['distribucion_dimensiones']['cocheras'] = self.get_cell_value(rowx=59,colx=41)

			data['tiempo_radicando'] = self.get_cell_value(rowx=60,colx=11)
			data['tipo_mobiliario'] = self.get_cell_value(rowx=60,colx=24)
			data['sector_socioeconomico'] = self.get_cell_value(rowx=60,colx=39)
			data['personas_viven_con_evaluado'] = self.get_cell_value(rowx=61,colx=12)
			data['conservacion'] = self.get_cell_value(rowx=62,colx=10)
			data['tamano_aprox_mts2'] = self.get_cell_value(rowx=62,colx=34)
			data['domicilio_anterior'] = self.get_cell_value(rowx=63,colx=20)
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de vivienda, revisar formato.')

		return data

	def getMarcoFamiliar(self):
		'''
			Función para extraer los datos referentes al marco familiar del precandidato
		'''
		data = {
					'padre': {},
					'madre': {},
					'hermano': [],
					'esposa': {},
					'hijo': [],
					'otro': []
				}
		try:
			data['padre']['nombre'] = self.get_cell_value(rowx=68,colx=4)
			data['padre']['edad'] = self.get_cell_value(rowx=68,colx=17)
			data['padre']['ocupacion'] = self.get_cell_value(rowx=68,colx=19)
			data['padre']['empresa'] = self.get_cell_value(rowx=68,colx=24)
			data['padre']['residencia'] = self.get_cell_value(rowx=68,colx=29)
			data['padre']['telefono'] = self.get_cell_value(rowx=68,colx=35)

			data['madre']['nombre'] = self.get_cell_value(rowx=69,colx=4)
			data['madre']['edad'] = self.get_cell_value(rowx=69,colx=17)
			data['madre']['ocupacion'] = self.get_cell_value(rowx=69,colx=19)
			data['madre']['empresa'] = self.get_cell_value(rowx=69,colx=24)
			data['madre']['residencia'] = self.get_cell_value(rowx=69,colx=29)
			data['madre']['telefono'] = self.get_cell_value(rowx=69,colx=35)

			
			data['hermano'].append({
					'nombre' : self.get_cell_value(rowx=70,colx=4),
					'edad' : self.get_cell_value(rowx=70,colx=17),
					'ocupacion' : self.get_cell_value(rowx=70,colx=19),
					'empresa' : self.get_cell_value(rowx=70,colx=24),
					'residencia' : self.get_cell_value(rowx=70,colx=29),
					'telefono' : self.get_cell_value(rowx=70,colx=35)
				}
			)

			data['hermano'].append({
					'nombre' : self.get_cell_value(rowx=71,colx=4),
					'edad' : self.get_cell_value(rowx=71,colx=17),
					'ocupacion' : self.get_cell_value(rowx=71,colx=19),
					'empresa' : self.get_cell_value(rowx=71,colx=24),
					'residencia' : self.get_cell_value(rowx=71,colx=29),
					'telefono' : self.get_cell_value(rowx=71,colx=35)
				}
			)

			data['hermano'].append({
					'nombre' : self.get_cell_value(rowx=72,colx=4),
					'edad' : self.get_cell_value(rowx=72,colx=17),
					'ocupacion' : self.get_cell_value(rowx=72,colx=19),
					'empresa' : self.get_cell_value(rowx=72,colx=24),
					'residencia' : self.get_cell_value(rowx=72,colx=29),
					'telefono' : self.get_cell_value(rowx=72,colx=35)
				}
			)

			data['hermano'].append({
					'nombre' : self.get_cell_value(rowx=73,colx=4),
					'edad' : self.get_cell_value(rowx=73,colx=17),
					'ocupacion' : self.get_cell_value(rowx=73,colx=19),
					'empresa' : self.get_cell_value(rowx=73,colx=24),
					'residencia' : self.get_cell_value(rowx=73,colx=29),
					'telefono' : self.get_cell_value(rowx=73,colx=35)
				}
			)

			data['esposa']['nombre'] = self.get_cell_value(rowx=74,colx=4)
			data['esposa']['edad'] = self.get_cell_value(rowx=74,colx=17)
			data['esposa']['ocupacion'] = self.get_cell_value(rowx=74,colx=19)
			data['esposa']['empresa'] = self.get_cell_value(rowx=74,colx=24)
			data['esposa']['residencia'] = self.get_cell_value(rowx=74,colx=29)
			data['esposa']['telefono'] = self.get_cell_value(rowx=74,colx=35)

			data['hijo'].append({
					'nombre' : self.get_cell_value(rowx=75,colx=4),
					'edad' : self.get_cell_value(rowx=75,colx=17),
					'ocupacion' : self.get_cell_value(rowx=75,colx=19),
					'empresa' : self.get_cell_value(rowx=75,colx=24),
					'residencia' : self.get_cell_value(rowx=75,colx=29),
					'telefono' : self.get_cell_value(rowx=75,colx=35)
				})

			data['hijo'].append({
					'nombre' : self.get_cell_value(rowx=76,colx=4),
					'edad' : self.get_cell_value(rowx=76,colx=17),
					'ocupacion' : self.get_cell_value(rowx=76,colx=19),
					'empresa' : self.get_cell_value(rowx=76,colx=24),
					'residencia' : self.get_cell_value(rowx=76,colx=29),
					'telefono' : self.get_cell_value(rowx=76,colx=35)
				})

			data['hijo'].append({
					'nombre' : self.get_cell_value(rowx=77,colx=4),
					'edad' : self.get_cell_value(rowx=77,colx=17),
					'ocupacion' : self.get_cell_value(rowx=77,colx=19),
					'empresa' : self.get_cell_value(rowx=77,colx=24),
					'residencia' : self.get_cell_value(rowx=77,colx=29),
					'telefono' : self.get_cell_value(rowx=77,colx=35)
				})

			data['hijo'].append({
					'nombre' : self.get_cell_value(rowx=78,colx=4),
					'edad' : self.get_cell_value(rowx=78,colx=17),
					'ocupacion' : self.get_cell_value(rowx=78,colx=19),
					'empresa' : self.get_cell_value(rowx=78,colx=24),
					'residencia' : self.get_cell_value(rowx=78,colx=29),
					'telefono' : self.get_cell_value(rowx=78,colx=35)
				})

			data['otro'].append({
					'parentesco': self.get_cell_value(rowx=79,colx=1),
					'nombre' : self.get_cell_value(rowx=79,colx=4),
					'edad' : self.get_cell_value(rowx=79,colx=17),
					'ocupacion' : self.get_cell_value(rowx=79,colx=19),
					'empresa' : self.get_cell_value(rowx=79,colx=24),
					'residencia' : self.get_cell_value(rowx=79,colx=29),
					'telefono' : self.get_cell_value(rowx=79,colx=35)
				})

			data['otro'].append({
					'parentesco': self.get_cell_value(rowx=79,colx=1),
					'nombre' : self.get_cell_value(rowx=80,colx=4),
					'edad' : self.get_cell_value(rowx=80,colx=17),
					'ocupacion' : self.get_cell_value(rowx=80,colx=19),
					'empresa' : self.get_cell_value(rowx=80,colx=24),
					'residencia' : self.get_cell_value(rowx=80,colx=29),
					'telefono' : self.get_cell_value(rowx=80,colx=35)
				})

			data['otro'].append({
					'parentesco': self.get_cell_value(rowx=79,colx=1),
					'nombre' : self.get_cell_value(rowx=81,colx=4),
					'edad' : self.get_cell_value(rowx=81,colx=17),
					'ocupacion' : self.get_cell_value(rowx=81,colx=19),
					'empresa' : self.get_cell_value(rowx=81,colx=24),
					'residencia' : self.get_cell_value(rowx=81,colx=29),
					'telefono' : self.get_cell_value(rowx=81,colx=35)
				})
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de marco familiar, revisar formato.')

		return data

	def getInfoEconomicaMensual(self):
		'''
			Función para extraer los datos económicos del precandidato
		'''
		data = {
					'ingresos': [],
					'egresos': []
				}

		try:
			#Ingresos
			data['ingresos'].append({	'concepto' : 'investigado',
										'monto' : self.get_cell_value(rowx=88,colx=9) })
			data['ingresos'].append({	'concepto' : 'conyuge',
										'monto' : self.get_cell_value(rowx=91,colx=9) })
			data['ingresos'].append({	'concepto' : 'padres',
										'monto' : self.get_cell_value(rowx=94,colx=9) })
			data['ingresos'].append({	'concepto' : 'hermanos',
										'monto' : self.get_cell_value(rowx=97,colx=9) })
			data['ingresos'].append({	'concepto' : 'otros',
										'monto' : self.get_cell_value(rowx=100,colx=9) })
			data['ingresos'].append({	'concepto' : 'total',
										'monto' : self.get_cell_value(rowx=102,colx=9) })
			#Egresos
			data['egresos'].append({	'concepto' : 'impuestos',
										'monto' : self.get_cell_value(rowx=88,colx=33) })
			data['egresos'].append({	'concepto' : 'vestimenta',
										'monto' : self.get_cell_value(rowx=89,colx=33) })
			data['egresos'].append({	'concepto' : 'gastos_automovil',
										'monto' : self.get_cell_value(rowx=90,colx=33) })
			data['egresos'].append({	'concepto' : 'transporte_publico',
										'monto' : self.get_cell_value(rowx=91,colx=33) })
			data['egresos'].append({	'concepto' : 'alimentacion',
										'monto' : self.get_cell_value(rowx=92,colx=33) })
			data['egresos'].append({	'concepto' : 'educacion',
										'monto' : self.get_cell_value(rowx=93,colx=33) })
			data['egresos'].append({	'concepto' : 'medico',
										'monto' : self.get_cell_value(rowx=94,colx=33) })
			data['egresos'].append({	'concepto' : 'diversos',
										'monto' : self.get_cell_value(rowx=95,colx=33) })
			data['egresos'].append({	'concepto' : 'servicios',
										'monto' : self.get_cell_value(rowx=96,colx=33) })
			data['egresos'].append({	'concepto' : 'serv_domestico',
										'monto' : self.get_cell_value(rowx=97,colx=33) })
			data['egresos'].append({	'concepto' : 'seguros',
										'monto' : self.get_cell_value(rowx=98,colx=33) })
			data['egresos'].append({	'concepto' : 'deuda1',
										'monto' : self.get_cell_value(rowx=99,colx=33) })
			data['egresos'].append({	'concepto' : 'deuda2',
										'monto' : self.get_cell_value(rowx=100,colx=33) })
			data['egresos'].append({	'concepto' : 'otros',
										'monto' : self.get_cell_value(rowx=101,colx=33) })
			data['egresos'].append({	'concepto' : 'total',
										'monto' : self.get_cell_value(rowx=102,colx=33) })
		except Exception, e:
			self.errors.append('No se pudo extraer los datos económicos mensuales, revisar formato.')

		return data

	def getSituacionEconomica(self):
		'''
			Función para extraer los datos bancarios y crédito del precandidato
		'''
		data = {
					'tarjetas_credito_comerciales': [],
					'cuentas_debito': [],
					'automoviles': [],
					'bienes_raices': [],
					'seguros': [],
					'deudas_actuales': []
				}
		try:
			data['tarjetas_credito_comerciales'].append({
				'institucion': self.get_cell_value(rowx=107,colx=1),
				'limite_credito': self.get_cell_value(rowx=107,colx=11),
				'pago_minimo': self.get_cell_value(rowx=107,colx=21),
				'saldo_actual': self.get_cell_value(rowx=107,colx=31)
	 		})

			data['tarjetas_credito_comerciales'].append({
					'institucion': self.get_cell_value(rowx=108,colx=1),
					'limite_credito': self.get_cell_value(rowx=108,colx=11),
					'pago_minimo': self.get_cell_value(rowx=108,colx=21),
					'saldo_actual': self.get_cell_value(rowx=108,colx=31)
		 		})

			data['cuentas_debito'].append({
					'institucion': self.get_cell_value(rowx=111,colx=1),
					'saldo_mensual': self.get_cell_value(rowx=111,colx=11),
					'antiguedad': self.get_cell_value(rowx=111,colx=21),
					'ahorro': self.get_cell_value(rowx=111,colx=31)
		 		})

			data['cuentas_debito'].append({
					'institucion': self.get_cell_value(rowx=112,colx=1),
					'saldo_mensual': self.get_cell_value(rowx=112,colx=11),
					'antiguedad': self.get_cell_value(rowx=112,colx=21),
					'ahorro': self.get_cell_value(rowx=112,colx=31)
		 		})

			data['automoviles'].append({
					'marca': self.get_cell_value(rowx=115,colx=1),
					'modelo_ano': self.get_cell_value(rowx=115,colx=11),
					'liquidacion': self.get_cell_value(rowx=115,colx=21),
					'valor_comercial': self.get_cell_value(rowx=115,colx=31)
		 		})

			data['automoviles'].append({
					'marca': self.get_cell_value(rowx=116,colx=1),
					'modelo_ano': self.get_cell_value(rowx=116,colx=11),
					'liquidacion': self.get_cell_value(rowx=116,colx=21),
					'valor_comercial': self.get_cell_value(rowx=116,colx=31)
		 		})

			data['bienes_raices'].append({
					'tipo_inmueble': self.get_cell_value(rowx=119,colx=1),
					'ubicacion': self.get_cell_value(rowx=119,colx=11),
					'liquidacion': self.get_cell_value(rowx=119,colx=21),
					'valor_comercial': self.get_cell_value(rowx=119,colx=31)
		 		})

			data['bienes_raices'].append({
					'tipo_inmueble': self.get_cell_value(rowx=120,colx=1),
					'ubicacion': self.get_cell_value(rowx=120,colx=11),
					'liquidacion': self.get_cell_value(rowx=120,colx=21),
					'valor_comercial': self.get_cell_value(rowx=120,colx=31)
		 		})

			data['seguros'].append({
					'empresa': self.get_cell_value(rowx=123,colx=1),
					'tipo': self.get_cell_value(rowx=123,colx=11),
					'forma_pago': self.get_cell_value(rowx=123,colx=21),
					'vigencia': self.get_cell_value(rowx=123,colx=31)
		 		})

			data['seguros'].append({
					'empresa': self.get_cell_value(rowx=124,colx=1),
					'tipo': self.get_cell_value(rowx=124,colx=11),
					'forma_pago': self.get_cell_value(rowx=124,colx=21),
					'vigencia': self.get_cell_value(rowx=124,colx=31)
		 		})

			data['deudas_actuales'].append({
					'fecha_otorgamiento': self.get_cell_value(rowx=128,colx=0),
					'tipo': self.get_cell_value(rowx=128,colx=7),
					'institucion': self.get_cell_value(rowx=128,colx=14),
					'cantidad_total': self.get_cell_value(rowx=128,colx=21),
					'saldo_actual': self.get_cell_value(rowx=128,colx=28),
					'pago_mensual': self.get_cell_value(rowx=128,colx=35)
		 		})

			data['deudas_actuales'].append({
					'fecha_otorgamiento': self.get_cell_value(rowx=129,colx=0),
					'tipo': self.get_cell_value(rowx=129,colx=7),
					'institucion': self.get_cell_value(rowx=129,colx=14),
					'cantidad_total': self.get_cell_value(rowx=129,colx=21),
					'saldo_actual': self.get_cell_value(rowx=129,colx=28),
					'pago_mensual': self.get_cell_value(rowx=129,colx=35)
		 		})
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de situación económica, revisar formato.')

		return data

	def getReferencias(self):
		'''
			Función para extraer las referencias personales del precandidato
		'''
		data = []
		try:
			data.append({
				'nombre': self.get_cell_value(rowx=137,colx=3),
				'domicilio': self.get_cell_value(rowx=138,colx=4),
				'telefono': self.get_cell_value(rowx=139,colx=4),
				'tiempo_conocido': self.get_cell_value(rowx=139,colx=26),
				'parentesco': self.get_cell_value(rowx=140,colx=4),
				'ocupacion': self.get_cell_value(rowx=140,colx=22),
				'lugares_labor_evaluado': self.get_cell_value(rowx=141,colx=18),
				'opinion': self.get_cell_value(rowx=143,colx=0),
				'tipo': 'vecinal'
			})

			data.append({
					'nombre': self.get_cell_value(rowx=150,colx=3),
					'domicilio': self.get_cell_value(rowx=151,colx=4),
					'telefono': self.get_cell_value(rowx=152,colx=4),
					'tiempo_conocido': self.get_cell_value(rowx=152,colx=26),
					'parentesco': self.get_cell_value(rowx=153,colx=4),
					'ocupacion': self.get_cell_value(rowx=153,colx=22),
					'lugares_labor_evaluado': self.get_cell_value(rowx=154,colx=18),
					'opinion': self.get_cell_value(rowx=155,colx=0),
					'tipo': 'personal'
				})
			
			data.append({
					'nombre': self.get_cell_value(rowx=163,colx=3),
					'domicilio': self.get_cell_value(rowx=164,colx=4),
					'telefono': self.get_cell_value(rowx=165,colx=4),
					'tiempo_conocido': '',
					'parentesco': self.get_cell_value(rowx=166,colx=4),
					'ocupacion': '',
					'lugares_labor_evaluado': '',
					'opinion': '',
					'tipo': 'personal_opcional'
				})
		except Exception, e:
			self.errors.append('No se pudo extraer los datos de referencias, revisar formato.')

		return data

	def getCuadroEvaluacion(self):
		'''
			Función para extraer los datos del cuadro de evaluación del precandidato
		'''
		data = {
					'documentos_cotejados': [],
					'aspectos_hogar': [],
					'aspectos_candidato': []
				}
		try:
				
			data['documentos_cotejados'].append({	'tipo' : 'acta_nacimiento',
													'estatus' : self.get_cell_value(rowx=215,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'acta_matrimonio',
													'estatus' : self.get_cell_value(rowx=216,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'comprobante_domicilio',
													'estatus' : self.get_cell_value(rowx=217,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'id_oficial',
													'estatus' : self.get_cell_value(rowx=218,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'comprobante_nss',
													'estatus' : self.get_cell_value(rowx=219,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'curp',
													'estatus' : self.get_cell_value(rowx=220,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'cartilla_smn',
													'estatus' : self.get_cell_value(rowx=221,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'ultimo_grado_estudio',
													'estatus' : self.get_cell_value(rowx=222,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'cartas_laborales',
													'estatus' : self.get_cell_value(rowx=223,colx=10)	})
			data['documentos_cotejados'].append({	'tipo' : 'motivos_falta_docs',
													'estatus' : '',
													'observaciones' : self.get_cell_value(rowx=226,colx=0)	})

			data['aspectos_hogar'].append({	'tipo' : 'orden',
											'estatus' : self.get_cell_value(rowx=218,colx=33)	})
			data['aspectos_hogar'].append({	'tipo' : 'limpieza',
											'estatus' : self.get_cell_value(rowx=219,colx=33)	})
			data['aspectos_hogar'].append({	'tipo' : 'conservacion',
											'estatus' : self.get_cell_value(rowx=220,colx=33) })

			data['aspectos_candidato'].append({	'tipo' : 'disponibilidad',
												'estatus' : self.get_cell_value(rowx=223,colx=33) })
			data['aspectos_candidato'].append({	'tipo' : 'puntualidad',
												'estatus' : self.get_cell_value(rowx=224,colx=33) })
			data['aspectos_candidato'].append({	'tipo' : 'apariencia_fisica',
												'estatus' : self.get_cell_value(rowx=225,colx=33) })
			data['aspectos_candidato'].append({	'tipo' : 'colaboracion',
												'estatus' : self.get_cell_value(rowx=226,colx=33) })
			data['aspectos_candidato'].append({	'tipo' : 'actitud',
												'estatus' : self.get_cell_value(rowx=227,colx=33) })											

		except Exception, e:
			self.errors.append('No se pudo extraer los datos de cuadro de evaluación, revisar formato.')

		return data

	def get_cell_value(self,rowx, colx):
		'''
			Función para obtener el dato de la celda independientemente a su tipo
		'''
		return_value = '***'
		
		cell_type = self.worksheet.cell_type(rowx=rowx, colx=colx)
		cell_value = self.worksheet.cell_value(rowx=rowx, colx=colx)
		
		#If cell_type is 'float' (2)
		if cell_type == 2:
			return_value = int(cell_value) if cell_value.is_integer() else cell_value
		#If cell_type is 'date' (3)
		elif cell_type == 3:
			try:
				return_value = datetime.datetime(*xlrd.xldate_as_tuple(self.worksheet.cell_value(rowx, colx), self.workbook.datemode)).date().strftime('%d/%m/%Y') 
			except Exception, e:
				try:
					return_value =  datetime.datetime.strptime(str(datetime.timedelta(days=cell_value)), '%H:%M:%S').strftime('%I:%M:%S %p')
				except Exception, e:
					return_value = cell_value
		#If cell_type is anything else (0,1,4,5,6)
		else:
			return_value = cell_value
	
		return unicode(return_value)

	def get_percentage(self, rowx, colx):
		'''
			Función para obtener el dato de la celda en valores tipo porcentaje, que pueden ser string, int o float
			cell_type
				0 is blank
				1 is text
				2 is a number
				3 is a date
		'''
		cell_type = self.worksheet.cell_type(rowx=rowx, colx=colx)
		cell_value = self.worksheet.cell_value(rowx=rowx, colx=colx)
		isFloat = False

		if cell_type == 2:
			if isinstance(cell_value, float):
				if int(cell_value) < 1:
					isFloat = True

		return_value = str(int(cell_value * 100)) if isFloat else str(cell_value)
		return unicode(return_value)

	"""docstring for ClassName"""
	def __init__(self):
		super(PreCandidato, self).__init__()
		self.errors = []
