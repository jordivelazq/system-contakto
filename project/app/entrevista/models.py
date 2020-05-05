# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from app.investigacion.models import Investigacion

ACTIVO_OPCIONES = (
	(1, 'SI'),
	(2, 'NO'),
	(0, 'NA'),
)

ARCHIVO_OPCIONES = (
	(0, 'Entrevista'),
	(1, 'Carga Masiva'),
	(2, 'Actualizacion Cobranza')
)

class EntrevistaFile(models.Model):
	record = models.FileField(verbose_name='Archivo', upload_to='xls')
	fecha_registro = models.DateField(auto_now=True)
	tipo = models.IntegerField(default=0, choices=ARCHIVO_OPCIONES, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.record

class EntrevistaPersona(models.Model):
	investigacion = models.ForeignKey(Investigacion)
	nombre = models.CharField(max_length=140, blank=True, null=True)
	apellido = models.CharField(max_length=140, blank=True, null=True)
	email = models.CharField(max_length=140, blank=True, null=True)
	nss = models.CharField(verbose_name='NSS (IMSS)', max_length=30, blank=True, null=True)
	edad = models.CharField(max_length=140, blank=True, null=True)
	curp = models.CharField(verbose_name='CURP', max_length=30, blank=True, null=True)
	rfc = models.CharField(verbose_name='RFC', max_length=30, blank=True, null=True)
	ife = models.CharField(verbose_name='Folio credencial IFE', max_length=30, blank=True, null=True)
	pasaporte = models.CharField(verbose_name='No. de pasaporte o visa', max_length=30, blank=True, null=True)
	smn = models.CharField(verbose_name='Cartilla SMN', max_length=30, blank=True, null=True)
	estado_civil = models.CharField( max_length=100, verbose_name='Estado civil', blank=True, null=True)
	fecha_matrimonio = models.CharField(verbose_name='Fecha de matrimonio', max_length=100, blank=True, null=True)
	religion = models.CharField(verbose_name='Religión', max_length=140, blank=True, null=True)
	religion_tiempo = models.CharField(verbose_name='Cada cuánto tiempo la practica', max_length=140, blank=True, null=True)
	tiempo_radicando = models.CharField(verbose_name='Tiempo radicando en la ciudad', max_length=140, blank=True, null=True)
	medio_utilizado = models.CharField(verbose_name='Medio que utiliza para transporte', max_length=140, blank=True, null=True)
	referencia_vacante = models.CharField(verbose_name='Medio por el qué se enteró de la vacante', max_length=140, blank=True, null=True)
	tiempo_transporte = models.CharField(verbose_name='Tiempo de trayecto al lugar de trabajo', max_length=140, blank=True, null=True)
	fecha_registro = models.DateField(auto_now=True)
	activa = models.BooleanField(default=True)
	dependientes_economicos = models.TextField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		return u'%s / %s' % (self.id, self.nombre)

class EntrevistaInvestigacion(models.Model):
	RESULTADO_OPCIONES = (
		('0', 'Por evaluar'),
		('1', 'Viable'),
		('2', 'Con reservas'),
		('3', 'No viable'),
	)
	investigacion = models.ForeignKey(Investigacion)
	agente = models.ForeignKey(User)
	persona = models.ForeignKey(EntrevistaPersona)
	empresa_contratante = models.CharField(max_length=140, blank=True, null=True)
	fecha_recibido = models.CharField(max_length=140, blank=True, null=True) #Del excel
	puesto = models.CharField(max_length=140, blank=True, null=True)
	fecha_registro = models.CharField(max_length=140, blank=True, null=True)
	conclusiones = models.TextField() # NOTA: posiblemente se puede borrar
	resultado = models.CharField(max_length=30, choices=RESULTADO_OPCIONES, blank=True, null=True)
	archivo = models.ForeignKey(EntrevistaFile, blank=True, null=True)
	folio = models.CharField(max_length=50, blank=True, null=True)
	presupuesto = models.CharField(max_length=50, blank=True, null=True)	

	def __unicode__(self):
		return u'%s / %s' % (self.persona, self.archivo)

'''
	Cita
'''
class EntrevistaCita(models.Model):
	investigacion = models.ForeignKey(Investigacion)
	fecha_entrevista = models.CharField(max_length=200, blank=True, null=True)
	hora_entrevista = models.CharField(max_length=200, blank=True, null=True)
	entrevistador = models.CharField(max_length=200, blank=True, null=True)
	autorizada = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)
	observaciones = models.TextField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (self.investigacion)

'''
	Modelos Datos Generales 
'''
class EntrevistaTelefono(models.Model):
	TELEFONO_OPCIONES = (
	    ('casa', 'casa'),
	    ('movil', 'movil'),
	    ('otro', 'otro'),
	    ('recado', 'recado'),
	)
	persona = models.ForeignKey(EntrevistaPersona)
	categoria = models.CharField(max_length=20, choices=TELEFONO_OPCIONES)
	numero = models.CharField(max_length=20, null=True, blank=True)
	parentesco = models.CharField(max_length=40, blank=True, null=True)

	def __unicode__(self):
		return self.numero

class EntrevistaDireccion(models.Model):
	investigacion = models.ForeignKey(Investigacion)
	persona = models.ForeignKey(EntrevistaPersona)
	calle = models.CharField(verbose_name='Calle', max_length=140, null=True, blank=True)
	num = models.CharField(verbose_name='Num ext-int', max_length=140, null=True, blank=True)
	ciudad = models.CharField(verbose_name='Ciudad', max_length=140, null=True, blank=True)
	colonia = models.CharField(verbose_name='Colonia o fraccionamiento', max_length=140, null=True, blank=True)
	cp = models.CharField(verbose_name='Código Postal', max_length=140, null=True, blank=True)
	estado = models.CharField(verbose_name='Estado', max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s, %s' % (self.calle, self.colonia, self.ciudad)

class EntrevistaPrestacionVivienda(models.Model):
	VIVIENDA_OPCIONES = (
		('infonavit', 'infonavit'),
		('fonacot', 'fonacot'),
	)
	persona = models.ForeignKey(EntrevistaPersona)
	categoria_viv = models.CharField(max_length=20, choices=VIVIENDA_OPCIONES)
	activo = models.CharField(verbose_name='Tiene crédito activo', max_length=140, null=True, blank=True)
	fecha_tramite = models.CharField(verbose_name='Fecha en que fue tramitado', max_length=140, null=True, blank=True)
	numero_credito = models.CharField(verbose_name='No. de crédito', max_length=140, null=True, blank=True)
	uso = models.CharField(max_length=250, null=True, blank=True)
	motivo = models.CharField(verbose_name='Para qué se tramitó?', max_length=250, null=True, blank=True)

	def __unicode__(self):
		return self.categoria_viv

class EntrevistaLicencia(models.Model):
	persona = models.ForeignKey(EntrevistaPersona)
	numero = models.CharField(verbose_name='No. de licencia', max_length=20, null=True, blank=True)
	tipo = models.CharField(verbose_name='Tipo de licencia', max_length=140, null=True, blank=True)
	
	def __unicode__(self):
		return '%s, %s' % (self.tipo, self.numero)

class EntrevistaOrigen(models.Model):
	persona = models.ForeignKey(EntrevistaPersona)
	lugar = models.CharField(verbose_name='Lugar de nacimiento', max_length=140, null=True, blank=True)
	nacionalidad = models.CharField(max_length=140, null=True, blank=True)
	fecha = models.CharField(verbose_name='Fecha de nacimiento', max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.lugar, self.fecha)


'''
	Modelos Info Personal
'''
class EntrevistaInfoPersonal(models.Model):
	persona = models.ForeignKey(EntrevistaPersona)
	antecedentes_penales = models.CharField(verbose_name='Demandas Laborales y/o Antecedentes Penales', max_length=500, null=True, blank=True)
	tatuajes = models.CharField(verbose_name='Cuenta con algún tatuaje o arete:(Cuantos y en que parte del cuerpo)', max_length=500, null=True, blank=True)


class EntrevistaHistorialEnEmpresa(models.Model):
	HISTORIAL_OPCIONES = (
	    ('trabajo', 'trabajo'),
	    ('familiar', 'familiar'),
	)
	TIENE_OPCIONES = (
	    ('SI', 'SI'),
	    ('NO', 'NO'),
	)
	persona = models.ForeignKey(EntrevistaPersona)
	categoria = models.CharField(max_length=20, choices=HISTORIAL_OPCIONES)
	tiene = models.CharField(max_length=140, null=True, blank=True, choices=TIENE_OPCIONES)
	puesto = models.CharField(max_length=500, null=True, blank=True)
	periodo = models.CharField(max_length=500, null=True, blank=True)	#Solo para categ. trabajo
	nombre = models.CharField(max_length=140, null=True, blank=True)	#Solo para cate. familiar
	sucursal = models.CharField(max_length=140, null=True, blank=True)
	motivo_salida = models.CharField(max_length=140, null=True, blank=True) #Solo para categ. trabajo
	parentesco = models.CharField(max_length=140, null=True, blank=True)	#Solo para cate. familiar

	def __unicode__(self):
		return '%s' % (self.tiene)
	

'''
	Modelos Salud/ActividadesHabitos
'''

class EntrevistaSalud(models.Model):
	persona = models.ForeignKey(EntrevistaPersona)
	peso_kg = models.CharField(max_length=200, null=True, blank=True)
	estatura_mts = models.CharField(max_length=200, null=True, blank=True)
	salud_fisica = models.CharField(max_length=200, null=True, blank=True)
	salud_visual = models.CharField(max_length=200, null=True, blank=True)
	embarazo_meses = models.CharField(max_length=200, null=True, blank=True)
	ejercicio_tipo_frecuencia = models.CharField(max_length=200, null=True, blank=True)
	accidentes = models.CharField(max_length=200, null=True, blank=True)
	intervenciones_quirurgicas = models.CharField(max_length=200, null=True, blank=True)
	enfermedades_familiares = models.CharField(max_length=200, null=True, blank=True)
	tratamiento_medico_psicologico = models.CharField(max_length=200, null=True, blank=True)
	enfermedades_mayor_frecuencia = models.CharField(max_length=200, null=True, blank=True)
	institucion_medica = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return '%s' % (self.peso_kg)

class EntrevistaActividadesHabitos(models.Model):
	persona = models.ForeignKey(EntrevistaPersona)
	inactividad_laboral = models.CharField(max_length=140, null=True, blank=True)
	inactividad_laboral_actividad = models.CharField(max_length=500, null=True, blank=True)
	negocios = models.CharField(max_length=140, null=True, blank=True)
	negocios_actividad = models.CharField(max_length=500, null=True, blank=True)
	frecuencia_tabaco = models.CharField(max_length=140, null=True, blank=True)
	frecuencia_alcohol = models.CharField(max_length=140, null=True, blank=True)
	frecuencia_otras_sust = models.CharField(max_length=140, null=True, blank=True)

'''
	Modelos información Académica
'''

class EntrevistaAcademica(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	cedula_profesional = models.CharField(max_length=200, null=True, blank=True)
	cedula_prof_ano_exp = models.CharField(max_length=200, null=True, blank=True)
	estudios_institucion = models.CharField(max_length=200, null=True, blank=True)
	estudios_que = models.CharField(max_length=200, null=True, blank=True)
	estudios_horarios = models.CharField(max_length=200, null=True, blank=True)
	estudios_dias = models.CharField(max_length=200, null=True, blank=True)
	activo = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, blank=True, null=True)

class EntrevistaGradoEscolaridad(models.Model):
	GRADO_OPCIONES = (
		('primaria' , 'Primaria'),
		('secundaria' , 'Secundaria'),
		('preparatoria' , 'Preparatoria'),
		('profesional' , 'Profesional'),
		('otro_grado' , 'Otro')
	)
	person = models.ForeignKey(EntrevistaPersona)
	grado = models.CharField(max_length=20, choices=GRADO_OPCIONES)
	institucion = models.CharField(max_length=200, null=True, blank=True)
	ciudad = models.CharField(max_length=200, null=True, blank=True)
	anos = models.CharField(max_length=200, null=True, blank=True)
	certificado = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return '%s' % (self.grado)

class EntrevistaOtroIdioma(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	hablado = models.CharField(max_length=140, null=True, blank=True)
	leido = models.CharField(max_length=140, null=True, blank=True)
	escuchado = models.CharField(max_length=140, null=True, blank=True)
	idioma = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s' % (self.idioma)

'''
	Modelos Situacion Vivienda
'''
class EntrevistaSituacionVivienda(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	tiempo_radicando = models.CharField(max_length=50, null=True, blank=True)
	tipo_mobiliario = models.CharField(max_length=200, null=True, blank=True)
	sector_socioeconomico = models.CharField(max_length=200, null=True, blank=True)
	personas_viven_con_evaluado = models.CharField(max_length=50, null=True, blank=True)
	conservacion = models.CharField(max_length=200, null=True, blank=True)
	tamano_aprox_mts2 = models.CharField(max_length=50, null=True, blank=True)
	domicilio_anterior = models.CharField(max_length=500, null=True, blank=True)
	domicilio_direcciones = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.tiempo_radicando, self.conservacion)

class EntrevistaPropietarioVivienda(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	nombre = models.CharField(verbose_name='Nombre del propietario' , max_length=200, null=True, blank=True)
	parentesco = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.nombre, self.parentesco)

class EntrevistaCaractaristicasVivienda(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	propia = models.CharField(max_length=50, null=True, blank=True)
	rentada = models.CharField(max_length=50, null=True, blank=True)
	hipotecada = models.CharField(max_length=50, null=True, blank=True)
	prestada = models.CharField(max_length=50, null=True, blank=True)
	otra = models.CharField(max_length=50, null=True, blank=True)
	valor_aproximado = models.CharField(max_length=50, null=True, blank=True)
	renta_mensual = models.CharField(max_length=50, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.propia, self.rentada)

class EntrevistaTipoInmueble(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	casa = models.CharField(max_length=50, null=True, blank=True)
	terreno_compartido = models.CharField(max_length=50, null=True, blank=True)
	departamento = models.CharField(max_length=50, null=True, blank=True)
	vivienda_popular = models.CharField(max_length=50, null=True, blank=True)
	otro_tipo = models.CharField(max_length=50, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.casa, self.departamento)

class EntrevistaDistribucionDimensiones(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	habitaciones = models.CharField(max_length=50, null=True, blank=True) 
	banos = models.CharField(max_length=50, null=True, blank=True)
	salas = models.CharField(max_length=50, null=True, blank=True)
	comedor = models.CharField(max_length=50, null=True, blank=True)
	cocina = models.CharField(max_length=50, null=True, blank=True)
	patios = models.CharField(max_length=50, null=True, blank=True)
	cocheras = models.CharField(max_length=50, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.habitaciones, self.banos)

'''
	Modelos Marco Familiar
'''
class EntrevistaMiembroMarcoFamiliar(models.Model):
	FAMILIAR_OPCIONES = (
		('padre', 'padre'),
		('madre', 'madre'),
		('hermano', 'hermano'),
		('pareja', 'pareja'),
		('hijo', 'hijo'),
		('otro', 'otro')
	)
	FAMILIAR_CATEGORIA = (
	    (1, 'Marco Familiar'),
	    (2, 'Vivienda'),
	)
	person = models.ForeignKey(EntrevistaPersona)
	tipo = models.CharField(max_length=20, choices=FAMILIAR_OPCIONES)
	nombre = models.CharField(max_length=140, null=True, blank=True)
	edad = models.CharField(max_length=140, null=True, blank=True)
	ocupacion = models.CharField(max_length=140, null=True, blank=True)
	empresa = models.CharField(max_length=140, null=True, blank=True)
	residencia = models.CharField(max_length=140, null=True, blank=True)
	telefono = models.CharField(max_length=140, null=True, blank=True)
	parentesco = models.CharField(max_length=140, null=True, blank=True)
	category = models.CharField(max_length=140, default=1, choices=FAMILIAR_OPCIONES)

	def __unicode__(self):
		return '%s' % self.tipo

'''
	Modelos Info Económica mensual
'''
class EntrevistaEconomica(models.Model):
	TIPO_OPCIONES = (
		('ingreso' , 'ingreso'),
		('egreso' , 'egreso')
	)
	person = models.ForeignKey(EntrevistaPersona)
	tipo = models.CharField(max_length=20, choices=TIPO_OPCIONES)
	concepto = models.CharField(max_length=140)
	detalle = models.CharField(max_length=140, null=True, blank=True)
	monto = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s - %s, %s, %s' % (self.person, self.tipo, self.concepto, self.monto)

'''
	Modelos Situación Económica
'''
class EntrevistaTarjetaCreditoComercial(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	institucion = models.CharField(max_length=140, null=True, blank=True)
	limite_credito = models.CharField(max_length=140, null=True, blank=True)
	pago_minimo = models.CharField(max_length=140, null=True, blank=True)
	saldo_actual = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.limite_credito)

class EntrevistaCuentaDebito(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	institucion = models.CharField(max_length=140, null=True, blank=True)
	saldo_mensual = models.CharField(max_length=140, null=True, blank=True)
	antiguedad = models.CharField(max_length=140, null=True, blank=True)
	ahorro = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.saldo_mensual)

class EntrevistaAutomovil(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	marca = models.CharField(max_length=140, null=True, blank=True)
	modelo_ano = models.CharField(max_length=140, null=True, blank=True)
	liquidacion = models.CharField(max_length=140, null=True, blank=True)
	valor_comercial = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.modelo_ano, self.liquidacion)

class EntrevistaBienesRaices(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	tipo_inmueble = models.CharField(max_length=140, null=True, blank=True)
	ubicacion = models.CharField(max_length=140, null=True, blank=True)
	liquidacion = models.CharField(max_length=140, null=True, blank=True)
	valor_comercial = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.tipo_inmueble, self.ubicacion)

class EntrevistaSeguro(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	empresa = models.CharField(max_length=140, null=True, blank=True)
	tipo = models.CharField(max_length=140, null=True, blank=True)
	forma_pago = models.CharField(max_length=140, null=True, blank=True)
	vigencia = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.empresa, self.tipo)

class EntrevistaDeudaActual(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	fecha_otorgamiento = models.CharField(max_length=140, null=True, blank=True)
	tipo = models.CharField(max_length=140, null=True, blank=True)
	institucion = models.CharField(max_length=140, null=True, blank=True)
	cantidad_total = models.CharField(max_length=140, null=True, blank=True)
	saldo_actual = models.CharField(max_length=140, null=True, blank=True)
	pago_mensual = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.saldo_actual)

'''
	Modelos Referencias
'''
class EntrevistaReferencia(models.Model):
	REFERENCIA_TIPO_OPCIONES = (
		('vecinal' , 'vecinal'),
		('personal' , 'personal'),
		('personal_opcional' , 'personal_opcional')
	)
	person = models.ForeignKey(EntrevistaPersona)
	nombre = models.CharField(max_length=140, blank=True, null=True)
	domicilio = models.CharField(max_length=200, blank=True, null=True)
	telefono = models.CharField(max_length=140, blank=True, null=True)
	tiempo_conocido = models.CharField(max_length=140, blank=True, null=True)
	parentesco = models.CharField(max_length=140, blank=True, null=True)
	ocupacion = models.CharField(max_length=140, blank=True, null=True)
	lugares_labor_evaluado = models.CharField(max_length=200, blank=True, null=True)
	opinion = models.TextField(max_length=500, blank=True, null=True)
	tipo = models.CharField(max_length=20, choices=REFERENCIA_TIPO_OPCIONES, default='')

	def __unicode__(self):
		return '%s, %s' % (self.nombre, self.parentesco)

'''
	Modelos Cuadro Evaluacion
'''

class EntrevistaDocumentoCotejado(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	tipo = models.CharField(max_length=255)
	estatus = models.BooleanField(default=False)
	observaciones = models.TextField(max_length=500, blank=True, null=True) #Solo se usa para el tipo 'motivos_falta_docs'

	def __unicode__(self):
			return '%s, %s' % (self.tipo, self.estatus)

class EntrevistaAspectoHogar(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	tipo = models.CharField(max_length=20)
	estatus = models.CharField(max_length=140, blank=True, null=True)

	def __unicode__(self):
			return '%s' % self.tipo

class EntrevistaAspectoCandidato(models.Model):
	person = models.ForeignKey(EntrevistaPersona)
	tipo = models.CharField(max_length=20)
	estatus = models.CharField(max_length=140, blank=True, null=True)

	def __unicode__(self):
			return '%s' % self.tipo
