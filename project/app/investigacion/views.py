# -*- coding: utf-8 -*-
import pdb
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from app.persona.models import Persona
from app.investigacion.models import Investigacion
from app.entrevista.models import EntrevistaInvestigacion

def get_telefonos(candidato):
	telefonos = candidato.telefono_set.all()
	tel_movil = telefonos.filter(categoria='movil')[0] if telefonos.filter(categoria='movil').count() else ''
	tel_casa = telefonos.filter(categoria='casa')[0] if telefonos.filter(categoria='casa').count() else ''
	tel_recado = telefonos.filter(categoria='recado')[0] if telefonos.filter(categoria='recado').count() else ''
	return tel_movil, tel_casa, tel_recado

@csrf_exempt
def print_reporte_laboral(request, investigacion_id):
	investigacion = Investigacion.objects.get(pk=investigacion_id)
	candidato = investigacion.candidato
	estado_civil = Persona.EDOCIVIL_OPCIONES[candidato.estado_civil][1]

	
	tel_movil, tel_casa, tel_recado = get_telefonos(candidato)

	trayectoria = candidato.trayectorialaboral_set.filter(status=True, visible_en_status=True)
	domicilio = candidato.direccion_set.all()[0] if candidato.direccion_set.all().count() else None
	
	origen = candidato.origen_set.all()[0] if candidato.origen_set.all().count() else None
	fecha_nacimiento = origen.fecha

	adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else None
	adjuntos_baseurl = settings.MEDIA_URL

	demanda = candidato.demanda_set.all()[0] if candidato.demanda_set.all().count() else None

	return render_to_response('sections/reportes/laboral/index.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def print_reporte_socioeconomico(request, investigacion_id):
	investigacion = Investigacion.objects.get(pk=investigacion_id)
	candidato = investigacion.candidato
	estado_civil = Persona.EDOCIVIL_OPCIONES[candidato.estado_civil][1]

	tel_movil, tel_casa, tel_recado = get_telefonos(candidato)
	

	trayectoria = candidato.trayectorialaboral_set.filter(status=True, visible_en_status=True)
	domicilio = investigacion.entrevistadireccion_set.all()[0] if investigacion.entrevistadireccion_set.all().count() else None

	adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else None
	adjuntos_baseurl = settings.MEDIA_URL

	demanda = candidato.demanda_set.all()[0] if candidato.demanda_set.all().count() else None

	entrevista_persona = investigacion.entrevistapersona_set.all()[0] if investigacion.entrevistapersona_set.all().count() else None

	origen = entrevista_persona.entrevistaorigen_set.get() if entrevista_persona.entrevistaorigen_set.all().count() else None

	entrevista_investigacion = investigacion.entrevistainvestigacion_set.all()[0] if investigacion.entrevistainvestigacion_set.all().count() else None
	entrevista_cita = investigacion.entrevistacita_set.all()[0] if investigacion.entrevistacita_set.all().count() else None

	licencia = entrevista_persona.entrevistalicencia_set.all()[0] if entrevista_persona.entrevistalicencia_set.all().count() else None
	historial_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='trabajo')[0] if entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='trabajo').count() else None
	historial_familiar_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='familiar')[0] if entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='familiar').count() else None
	info_personal = entrevista_persona.entrevistainfopersonal_set.all()[0] if entrevista_persona.entrevistainfopersonal_set.all().count() else None
	salud = entrevista_persona.entrevistasalud_set.all()[0] if entrevista_persona.entrevistasalud_set.all().count() else None
	actividades_habitos = entrevista_persona.entrevistaactividadeshabitos_set.all()[0] if entrevista_persona.entrevistaactividadeshabitos_set.all().count() else None

	#ADADEMICA
	info_academica = entrevista_persona.entrevistaacademica_set.all()[0] if entrevista_persona.entrevistaacademica_set.all().count() else None
	info_academica_grados = entrevista_persona.entrevistagradoescolaridad_set.all() if entrevista_persona.entrevistagradoescolaridad_set.all().count() else None
	info_academica_idioma = entrevista_persona.entrevistaotroidioma_set.all()[0] if entrevista_persona.entrevistaotroidioma_set.all().count() else None

	referencias = entrevista_persona.entrevistareferencia_set.all() if entrevista_persona.entrevistareferencia_set.all().count() else None

	marco_familiar = entrevista_persona.entrevistamiembromarcofamiliar_set.all() if entrevista_persona.entrevistamiembromarcofamiliar_set.all().count() else None

	# vivienda
	situacion_vivienda = entrevista_persona.entrevistasituacionvivienda_set.get()
	propietario_vivienda = entrevista_persona.entrevistapropietariovivienda_set.get()
	caracteristicas_vivienda = entrevista_persona.entrevistacaractaristicasvivienda_set.get()
	tipo_inmueble_vivienda = entrevista_persona.entrevistatipoinmueble_set.get()
	distribucion_vivienda = entrevista_persona.entrevistadistribuciondimensiones_set.get()

	# economica
	ingresos = entrevista_persona.entrevistaeconomica_set.filter(tipo='ingreso')
	egresos = entrevista_persona.entrevistaeconomica_set.filter(tipo='egreso')

	tarjeta_credito = entrevista_persona.entrevistatarjetacreditocomercial_set.all()
	tarjeta_debito = entrevista_persona.entrevistacuentadebito_set.all()
	automoviles = entrevista_persona.entrevistaautomovil_set.all()
	bienes_raices = entrevista_persona.entrevistabienesraices_set.all()
	seguros = entrevista_persona.entrevistaseguro_set.all()
	deudas = entrevista_persona.entrevistadeudaactual_set.all()

	infonavit = entrevista_persona.entrevistaprestacionvivienda_set.get(categoria_viv='infonavit') if entrevista_persona.entrevistaprestacionvivienda_set.filter(categoria_viv='infonavit').count() else None
	fonacot = entrevista_persona.entrevistaprestacionvivienda_set.get(categoria_viv='fonacot') if entrevista_persona.entrevistaprestacionvivienda_set.filter(categoria_viv='fonacot').count() else None

	return render_to_response('sections/reportes/socioeconomico/index.html', locals(), context_instance=RequestContext(request))
