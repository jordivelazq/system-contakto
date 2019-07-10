# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from app.persona.models import Persona
from app.investigacion.models import Investigacion
from app.entrevista.models import EntrevistaInvestigacion

@csrf_exempt
def print_reporte_laboral(request, investigacion_id):
	investigacion = Investigacion.objects.get(pk=investigacion_id)
	candidato = investigacion.candidato
	estado_civil = Persona.EDOCIVIL_OPCIONES[candidato.estado_civil][1]

	
	telefonos = candidato.telefono_set.all()
	tel_movil = telefonos.filter(categoria='movil')[0] if telefonos.filter(categoria='movil').count() else ''
	tel_casa = telefonos.filter(categoria='casa')[0] if telefonos.filter(categoria='casa').count() else ''
	tel_recado = telefonos.filter(categoria='recado')[0] if telefonos.filter(categoria='recado').count() else ''

	trayectoria = candidato.trayectorialaboral_set.filter(status=True, visible_en_status=True)
	domicilio = candidato.direccion_set.all()[0]
	
	origen = candidato.origen_set.all()[0]
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

	
	telefonos = candidato.telefono_set.all()
	tel_movil = telefonos.filter(categoria='movil')[0] if telefonos.filter(categoria='movil').count() else ''
	tel_casa = telefonos.filter(categoria='casa')[0] if telefonos.filter(categoria='casa').count() else ''
	tel_recado = telefonos.filter(categoria='recado')[0] if telefonos.filter(categoria='recado').count() else ''

	trayectoria = candidato.trayectorialaboral_set.filter(status=True, visible_en_status=True)
	domicilio = candidato.direccion_set.all()[0]
	
	origen = candidato.origen_set.all()[0]
	fecha_nacimiento = origen.fecha

	adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else None
	adjuntos_baseurl = settings.MEDIA_URL

	demanda = candidato.demanda_set.all()[0] if candidato.demanda_set.all().count() else None

	entrevista_persona = investigacion.entrevistapersona_set.all()[0]

	entrevista_investigacion = investigacion.entrevistainvestigacion_set.all()[0]
	entrevista_cita = investigacion.entrevistacita_set.all()[0]

	licencia = entrevista_persona.entrevistalicencia_set.all()[0]
	historial_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='trabajo')[0]
	historial_familiar_en_empresa = entrevista_persona.entrevistahistorialenempresa_set.filter(categoria='familiar')[0]
	info_personal = entrevista_persona.entrevistainfopersonal_set.all()[0]
	salud = entrevista_persona.entrevistasalud_set.all()[0]
	actividades_habitos = entrevista_persona.entrevistaactividadeshabitos_set.all()[0]

	#ADADEMICA
	info_academica = entrevista_persona.entrevistaacademica_set.all()[0]
	info_academica_grados = entrevista_persona.entrevistagradoescolaridad_set.all()
	info_academica_idioma = entrevista_persona.entrevistaotroidioma_set.all()[0]


	return render_to_response('sections/reportes/socioeconomico/index.html', locals(), context_instance=RequestContext(request))
