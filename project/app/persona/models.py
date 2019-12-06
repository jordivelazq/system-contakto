# -*- coding: utf-8 -*-

from django.db import models
from app.compania.models import Compania, Sucursales
from django.core.exceptions import ValidationError

ACTIVO_OPCIONES = (
	(0, 'Sí/No'),
	(1, 'Sí'),
	(2, 'No'),
)

ESTADOSMEXICO_OPCIONES = (
	("Aguascalientes", "Aguascalientes"),
	("Baja California", "Baja California"),
	("Baja California Sur", "Baja California Sur"),
	("Campeche", "Campeche"),
	("Chiapas", "Chiapas"),
	("Chihuahua", "Chihuahua"),
	("Coahuila", "Coahuila"),
	("Colima", "Colima"),
	("Distrito Federal", "Distrito Federal"),
	("Durango", "Durango"),
	("Estado de Mexico", "Estado de México"),
	("Guanajuato", "Guanajuato"),
	("Guerrero", "Guerrero"),
	("Hidalgo", "Hidalgo"),
	("Jalisco", "Jalisco"),
	("Michoacán", "Michoacán"),
	("Morelos", "Morelos"),
	("Nayarit", "Nayarit"),
	("Nuevo León", "Nuevo León"),
	("Oaxaca", "Oaxaca"),
	("Puebla", "Puebla"),
	("Querétaro", "Querétaro"),
	("Quintana Roo", "Quintana Roo"),
	("San Luis Potosí", "San Luis Potosí"),
	("Sinaloa", "Sinaloa"),
	("Sonora", "Sonora"),
	("Tabasco", "Tabasco"),
	("Tamaulipas", "Tamaulipas"),
	("Tlaxcala", "Tlaxcala"),
	("Veracruz", "Veracruz"),
	("Yucatán", "Yucatán"),
	("Zacatecas", "Zacatecas"),
)

class File(models.Model):
	record = models.FileField(verbose_name="Archivo", upload_to="xls")
	fecha_registro = models.DateField(auto_now=True)

def validate_nss(nss):
	if nss != '' and len(nss) != 11:
		raise ValidationError('NSS debe tener 11 caracteres')

def validate_curp(curp):
	if curp != '' and len(curp) != 18:
		raise ValidationError('CURP debe tener 18 caracteres')

class Persona(models.Model):
	EDOCIVIL_OPCIONES = (
	    (0, 'Soltero(a)'),
	    (1, 'Casado(a)'),
	    (2, 'Divorciado(a)'),
	)
	EDAD_CHOICES = [(i,i) for i in range(15, 76)]
	nombre = models.CharField(max_length=140)
	apellido = models.CharField(max_length=140, default="")
	nss = models.CharField(max_length=30, blank=True, null=True, validators=[validate_nss]) #validación de único desde views para aceptar valores vacios
	email = models.EmailField(max_length=140, blank=True, null=True)
	edad = models.IntegerField( blank=True, null=True) #choices=EDAD_CHOICES,
	curp = models.CharField(max_length=30, blank=True, null=True, validators=[validate_curp]) #validación de único desde views para aceptar valores vacios

	# datos extras del excel
	rfc = models.CharField(max_length=30, blank=True, null=True)
	ife = models.CharField(max_length=30, blank=True, null=True)
	pasaporte = models.CharField(max_length=30, blank=True, null=True)
	smn = models.CharField(max_length=30, blank=True, null=True)
	estado_civil = models.IntegerField(default=0, choices=EDOCIVIL_OPCIONES, blank=True, null=True)
	fecha_matrimonio = models.DateField(blank=True, null=True)
	religion = models.CharField(max_length=140, blank=True, null=True)
	tiempo_radicando = models.CharField(max_length=140, blank=True, null=True)
	medio_utilizado = models.CharField(max_length=140, blank=True, null=True)
	fecha_registro = models.DateField(auto_now=True)
	estatus = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

'''
	Modelos Datos Generales
'''
class Telefono(models.Model):
	TELEFONO_OPCIONES = (
	    ('casa', 'casa'),
	    ('movil', 'movil'),
	    ('otro', 'otro'),
	    ('recado', 'recado'),
	)
	persona = models.ForeignKey(Persona)
	categoria = models.CharField(max_length=20, choices=TELEFONO_OPCIONES)
	numero = models.CharField(max_length=14, null=True, blank=True)
	parentesco = models.CharField(max_length=40, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.numero)

class Direccion(models.Model):
	persona = models.ForeignKey(Persona)
	calle = models.CharField(max_length=140, null=True, blank=True)
	ciudad = models.CharField(max_length=140, null=True, blank=True)
	colonia = models.CharField(max_length=140, null=True, blank=True)
	cp = models.CharField(max_length=140, null=True, blank=True)
	estado = models.CharField(max_length=140, default="Baja California", choices=ESTADOSMEXICO_OPCIONES)

	def __unicode__(self):
		return '%s, %s, %s' % (self.calle, self.colonia, self.ciudad)

class PrestacionVivienda(models.Model):
	VIVIENDA_OPCIONES = (
	    ('infonavit', 'infonavit'),
	    ('fonacot', 'fonacot'),
	)
	persona = models.ForeignKey(Persona)
	categoria_viv = models.CharField(max_length=20, choices=VIVIENDA_OPCIONES)
	activo = models.IntegerField(default=0, choices=ACTIVO_OPCIONES, null=True, blank=True)
	fecha_tramite = models.DateField(null=True, blank=True)
	numero_credito = models.CharField(max_length=140, null=True, blank=True)
	uso = models.CharField(max_length=250, null=True, blank=True)

	def __unicode__(self):
		return u'%s - %s' % (self.persona, self.categoria_viv)

class Licencia(models.Model):
	persona = models.ForeignKey(Persona)
	numero = models.CharField(max_length=20)
	tipo = models.CharField(max_length=14)
	
	def __unicode__(self):
		return '%s, %s' % (self.tipo, self.numero)

class Origen(models.Model):
	persona = models.ForeignKey(Persona)
	lugar = models.CharField(max_length=140, null=True, blank=True)
	nacionalidad = models.CharField(max_length=140, null=True, blank=True)
	fecha = models.DateField(null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.lugar, self.fecha)


'''
	Modelos Info Personal
'''

class InfoPersonal(models.Model):
	persona = models.ForeignKey(Persona)
	tatuajes = models.CharField(max_length=500)

class TrayectoriaLaboral(models.Model):
	SALIDA_OPCIONES = (
	    ('0', 'Renuncia voluntaria'),
	    ('1', 'Recisión de contrato'),
	    ('2', 'Ausentismo'),
	    ('3', 'Término de contrato'),
	    ('4', 'Recorte de personal'),
	    ('5', 'Activo'),
	    ('6', 'Otro'),
	)
	# información que viene del doc
	persona = models.ForeignKey(Persona)
	compania = models.ForeignKey(Compania)
	sucursal = models.ForeignKey(Sucursales, null=True, blank=True)
	aparece_nss = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)

	reporta_candidato = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)

	puesto_inicial = models.CharField(max_length=140, null=True, blank=True)
	puesto_final = models.CharField(max_length=140, null=True, blank=True)
	periodo_alta = models.CharField(max_length=140, null=True, blank=True)
	periodo_baja = models.CharField(max_length=140, null=True, blank=True)
	reingreso_inicial = models.CharField(max_length=140, null=True, blank=True)
	reingreso_final = models.CharField(max_length=140, null=True, blank=True)

	sueldo_inicial = models.CharField(max_length=140, null=True, blank=True)
	sueldo_final = models.CharField(max_length=140, null=True, blank=True) #NUEVO

	funciones = models.TextField(null=True, blank=True)

	cumplio_objetivos = models.TextField(null=True, blank=True)#NUEVO

	motivo_salida = models.CharField(max_length=140, choices=SALIDA_OPCIONES, null=True, blank=True)
	no_personas_cargo = models.CharField(max_length=140, null=True, blank=True)
	recontratable = models.CharField(max_length=140, null=True, blank=True)

	terminada = models.BooleanField(default=False)
	visible_en_status = models.BooleanField(default=True)
	observaciones_generales = models.TextField(null=True, blank=True)

	status = models.BooleanField(default=True)

	def __unicode__(self):
		return  u'%s/%s' % (self.persona, self.compania)

	def getMotivoSalida(self):
		for option in self.SALIDA_OPCIONES:
			if option[0] == self.motivo_salida:
				return option[1].decode('utf-8').upper()
		return ''
	
	def opinion_rh(self):
		if self.opinion_set.filter(categoria=2).count():
			return self.opinion_set.filter(categoria=2)[0]
		return None
	
	def opinion_jefe(self):
		if self.opinion_set.filter(categoria=1).count():
			return self.opinion_set.filter(categoria=1)[0]
		return None

class CartaLaboral(models.Model):
	trayectoriaLaboral = models.OneToOneField(TrayectoriaLaboral)
	tiene_carta = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)
	expide = models.CharField(max_length=140, null=True, blank=True)
	fecha = models.CharField(max_length=140, null=True, blank=True)

class DatosGenerales(models.Model):
	trayectoriaLaboral = models.OneToOneField(TrayectoriaLaboral)
	num_personas = models.CharField(max_length=140, null=True, blank=True)
	puestos = models.CharField(max_length=140, null=True, blank=True)
	tiene_valores = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)
	motivo_salida = models.CharField(max_length=140, null=True, blank=True)
	motivo_salida_candidato = models.CharField(max_length=140, null=True, blank=True)
	tiene_sindicato = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)
	nombre_sindicato = models.CharField(max_length=140, null=True, blank=True)
	es_recontratable = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)
	recontratable_motivo = models.CharField(max_length=140, null=True, blank=True)
	tiene_mercancia = models.BooleanField(default=False)
	tiene_informacion = models.BooleanField(default=False)
	tiene_documentos = models.BooleanField(default=False)
	tiene_efectivo = models.BooleanField(default=False)

class Legalidad(models.Model):
	persona = models.ForeignKey(Persona)
	sindicato = models.CharField(max_length=500, null=True, blank=True)
	afiliado_sindicato = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)

	def __unicode__(self):
		return '%s, %s' % (self.persona, self.sindicato)

class Demanda(models.Model):
	persona = models.ForeignKey(Persona)
	tiene_demanda = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)
	empresa = models.CharField(max_length=500, null=True, blank=True)
	motivo = models.CharField(max_length=500, null=True, blank=True)
	ubicacion = models.CharField(max_length=500, null=True, blank=True)
	fecha = models.CharField(max_length=500, null=True, blank=True)
	audiencias = models.CharField(max_length=500, null=True, blank=True)
	conclusion = models.CharField(max_length=500, null=True, blank=True)

class Seguro(models.Model):
	persona = models.ForeignKey(Persona)
	verificado_enburo = models.IntegerField(default=0, choices=ACTIVO_OPCIONES)

	def __unicode__(self):
		return '%s' % (self.persona)

'''
	Modelos Salud/ActividadesHabitos
'''

class Salud(models.Model):
	persona = models.ForeignKey(Persona)
	peso_kg = models.FloatField()
	estatura_mts = models.FloatField()
	salud_fisica = models.CharField(max_length=200)
	salud_visual = models.CharField(max_length=200)
	embarazo_meses = models.CharField(max_length=200)
	ejercicio_tipo_frecuencia = models.CharField(max_length=200)
	accidentes = models.CharField(max_length=200)
	intervenciones_quirurgicas = models.CharField(max_length=200)
	enfermedades_familiares = models.CharField(max_length=200)
	tratamiento_medico_psicologico = models.CharField(max_length=200)
	enfermedades_mayor_frecuencia = models.CharField(max_length=200)
	institucion_medica = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s, %s' % (self.enfermedades_mayor_frecuencia, self.enfermedades_familiares)

class ActividadesHabitos(models.Model):
	persona = models.ForeignKey(Persona)
	tiempo_libre = models.CharField(max_length=140)
	extras = models.CharField(max_length=140)
	frecuencia_tabaco = models.CharField(max_length=140)
	frecuencia_alcohol = models.CharField(max_length=140)
	frecuencia_otras_sust = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s' % (self.tiempo_libre)

'''
	Modelos información Académica
'''

class Academica(models.Model):
	person = models.ForeignKey(Persona)
	cedula_profesional = models.CharField(max_length=200)
	cedula_prof_ano_exp = models.CharField(max_length=200)
	estudios_actuales = models.CharField(max_length=200)
	
	def __unicode__(self):
		return '%s' % (self.estudios_actuales)

class GradoEscolaridad(models.Model):
	GRADO_OPCIONES = (
	    ('primaria' , 'primaria'),
		('secundaria' , 'secundaria'),
		('preparatoria' , 'preparatoria'),
		('profesional' , 'profesional'),
		('otro_grado' , 'otro_grado')
	)
	person = models.ForeignKey(Persona)
	grado = models.CharField(max_length=20, choices=GRADO_OPCIONES)
	institucion = models.CharField(max_length=200)
	ciudad = models.CharField(max_length=200)
	anos = models.CharField(max_length=200)
	certificado = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s, %s' % (self.grado, self.institucion)

class OtroIdioma(models.Model):
	person = models.ForeignKey(Persona)
	porcentaje = models.IntegerField();
	idioma = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.idioma, self.porcentaje)

'''
	Modelos Situacion Vivienda
'''
class SituacionVivienda(models.Model):
	person = models.ForeignKey(Persona)
	tiempo_radicando = models.CharField(max_length=50)
	tipo_mobiliario = models.CharField(max_length=200)
	sector_socioeconomico = models.CharField(max_length=200)
	personas_viven_con_evaluado = models.CharField(max_length=50)
	conservacion = models.CharField(max_length=200)
	tamano_aprox_mts2 = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s, %s' % (self.tiempo_radicando, self.conservacion)

class PropietarioVivienda(models.Model):
	person = models.ForeignKey(Persona)
	nombre = models.CharField(max_length=200)
	parentesco = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s, %s' % (self.nombre, self.parentesco)

class CaractaristicasVivienda(models.Model):
	person = models.ForeignKey(Persona)
	propia = models.CharField(max_length=50)
	rentada = models.CharField(max_length=50)
	hipotecada = models.CharField(max_length=50)
	prestada = models.CharField(max_length=50)
	otra = models.CharField(max_length=50)
	valor_aproximado = models.CharField(max_length=50)
	renta_mensual = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s, %s' % (self.propia, self.rentada)

class TipoInmueble(models.Model):
	person = models.ForeignKey(Persona)
	casa = models.CharField(max_length=50)
	terreno_compartido = models.CharField(max_length=50)
	departamento = models.CharField(max_length=50)
	vivienda_popular = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s, %s' % (self.casa, self.departamento)

class DistribucionDimensiones(models.Model):
	person = models.ForeignKey(Persona)
	habitaciones = models.CharField(max_length=50) 
	banos = models.CharField(max_length=50)
	salas = models.CharField(max_length=50)
	comedor = models.CharField(max_length=50)
	cocina = models.CharField(max_length=50)
	patios = models.CharField(max_length=50)
	cocheras = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s, %s' % (self.habitaciones, self.banos)

'''
	Modelos Marco Familiar
'''
class MiembroMarcoFamiliar(models.Model):
	FAMILIAR_OPCIONES = (
		('padre', 'padre'),
		('madre', 'madre'),
		('hermano', 'hermano'),
		('pareja', 'pareja'),
		('hijo', 'hijo'),
		('otro', 'otro')
	)
	person = models.ForeignKey(Persona)
	tipo = models.CharField(max_length=20, choices=FAMILIAR_OPCIONES)
	nombre = models.CharField(max_length=140)
	edad = models.CharField(max_length=140, null=True, blank=True)
	ocupacion = models.CharField(max_length=140, null=True, blank=True)
	empresa = models.CharField(max_length=140, null=True, blank=True)
	residencia = models.CharField(max_length=140, null=True, blank=True)
	telefono = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return '%s, %s' % (self.tipo, self.nombre)

'''
	Modelos Info Económica mensual
'''
class Economica(models.Model):
	TIPO_OPCIONES = (
	    ('ingreso' , 'ingreso'),
		('egreso' , 'egreso')
	)
	person = models.ForeignKey(Persona)
	tipo = models.CharField(max_length=20, choices=TIPO_OPCIONES)
	concepto = models.CharField(max_length=140)
	monto = models.FloatField()

	def __unicode__(self):
		return '%s, %s, %s' % (self.tipo, self.concepto, self.monto)

'''
	Modelos Situación Económica
'''
class TarjetaCreditoComercial(models.Model):
	person = models.ForeignKey(Persona)
	institucion = models.CharField(max_length=140)
	limite_credito = models.CharField(max_length=140)
	pago_minimo = models.CharField(max_length=140)
	saldo_actual = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.limite_credito)

class CuentaDebito(models.Model):
	person = models.ForeignKey(Persona)
	institucion = models.CharField(max_length=140)
	saldo_mensual = models.CharField(max_length=140)
	antiguedad = models.CharField(max_length=140)
	ahorro = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.saldo_mensual)

class Automovil(models.Model):
	person = models.ForeignKey(Persona)
	marca = models.CharField(max_length=140)
	modelo_ano = models.CharField(max_length=140)
	liquidacion = models.CharField(max_length=140)
	valor_comercial = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.modelo_ano, self.liquidacion)

class BienesRaices(models.Model):
	person = models.ForeignKey(Persona)
	tipo_inmueble = models.CharField(max_length=140)
	ubicacion = models.CharField(max_length=140)
	liquidacion = models.CharField(max_length=140)
	valor_comercial = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.tipo_inmueble, self.ubicacion)

class Seguro(models.Model):
	person = models.ForeignKey(Persona)
	empresa = models.CharField(max_length=140)
	tipo = models.CharField(max_length=140)
	forma_pago = models.CharField(max_length=140)
	vigencia = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.empresa, self.tipo)

class DeudaActual(models.Model):
	person = models.ForeignKey(Persona)
	fecha_otorgamiento = models.DateField(null=True, blank=True)
	tipo = models.CharField(max_length=140)
	institucion = models.CharField(max_length=140)
	cantidad_total = models.CharField(max_length=140)
	saldo_actual = models.CharField(max_length=140)
	pago_mensual = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.institucion, self.saldo_actual)

'''
	Modelos Referencias
'''
class Referencia(models.Model):
	person = models.ForeignKey(Persona)
	nombre = models.CharField(max_length=140)
	domicilio = models.CharField(max_length=200)
	telefono = models.CharField(max_length=140)
	tiempo_conocido = models.CharField(max_length=140)
	parentesco = models.CharField(max_length=140)
	ocupacion = models.CharField(max_length=140)
	lugares_labor_evaluado = models.CharField(max_length=200)
	opinion = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s, %s' % (self.nombre, self.parentesco)

'''
	Modelos Cuadro Evaluacion
'''
class CuadroEvaluacion(models.Model):
	person = models.ForeignKey(Persona)
	conclusiones = models.TextField()
	viable = models.CharField(max_length=140) 
	no_viable = models.CharField(max_length=140) 
	reservas = models.CharField(max_length=140) 

	def __unicode__(self):
		return '%s, %s' % (self.conclusiones, self.reservas)

class DocumentoCotejado(models.Model):
	person = models.ForeignKey(Persona)
	tipo = models.CharField(max_length=20)
	estatus = models.CharField(max_length=140)

	def __unicode__(self):
			return '%s, %s' % (self.tipo, self.estatus)

class AspectoHogar(models.Model):
	person = models.ForeignKey(Persona)
	tipo = models.CharField(max_length=20)
	estatus = models.CharField(max_length=140)

	def __unicode__(self):
			return '%s, %s' % (self.tipo, self.estatus)

class AspectoCandidato(models.Model):
	person = models.ForeignKey(Persona)
	tipo = models.CharField(max_length=20)
	estatus = models.CharField(max_length=140)

	def __unicode__(self):
		return '%s, %s' % (self.tipo, self.estatus)

# Datos del word
class Evaluacion(models.Model):
	EVALUACION_OPCIONES = (
		('1', 'Excelente'),
		('2', 'Bueno'),
		('3', 'Regular'),
		('4', 'Malo'),
	)
	trayectoriaLaboral = models.ForeignKey(TrayectoriaLaboral)
	productividad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	adaptabilidad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	motivacion = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	puntualidad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	asistencia = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	disponibilidad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	responsabilidad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	relacion_jefe_inmediato = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	relacion_companeros = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	compromiso = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	honestidad = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	toma_decisiones = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)
	solucion_problemas = models.CharField(max_length=20, choices=EVALUACION_OPCIONES, null=True, blank=True)

	def __unicode__(self):
		return  '%s' % (self.trayectoriaLaboral)

class Opinion(models.Model):
	OPINION_OPCIONES = (
		(1, 'Jefe'),
		(2, 'Recursos Humanos'),
	)
	trayectoriaLaboral = models.ForeignKey(TrayectoriaLaboral)
	categoria = models.IntegerField(default=0, choices=OPINION_OPCIONES)
	opinion = models.TextField(null=True, blank=True)
	nombre = models.CharField(max_length=140, null=True, blank=True)
	puesto = models.CharField(max_length=140, null=True, blank=True)
	telefono = models.CharField(max_length=140, null=True, blank=True)
	email = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return  '%s' % (self.trayectoriaLaboral)

class Informante(models.Model):
	evaluacion = models.ForeignKey(Evaluacion)
	nombre = models.CharField(max_length=140, null=True, blank=True)
	puesto = models.CharField(max_length=140, null=True, blank=True)

	def __unicode__(self):
		return  '%s' % (self.evaluacion)
