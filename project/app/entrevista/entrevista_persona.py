# -*- coding: utf-8 -*-

from app.entrevista.models import *
from app.investigacion.models import Investigacion
from app.compania.models import *
from app.persona.models import Persona
from app.entrevista.services import EntrevistaService


class EntrevistaPersonaService():
    def __init__(self, investigacion_id=1):
        self.investigacion_id = investigacion_id

    def verifyData(self):
        print('verifyData')
        try:
            investigacion = Investigacion.objects.get(pk=self.investigacion_id)
            ep, create = EntrevistaPersona.objects.get_or_create(investigacion_id=self.investigacion_id)

            if not create:
                print('EntrevistaPersona existente')
                return False
            
        except EntrevistaPersona.DoesNotExist:
            print('No existe investifacion')
            return False
        
        print(ep, "Persona: " , "Se creo", create)
        EntrevistaDireccion.objects.get_or_create(investigacion_id=self.investigacion_id, persona_id=ep.pk)
        EntrevistaAcademica.objects.get_or_create(person_id=ep.pk)
        EntrevistaActividadesHabitos.objects.get_or_create(persona_id=ep.pk)
        EntrevistaBienesRaices.objects.get_or_create(person_id=ep.pk) 
        EntrevistaDeudaActual.objects.get_or_create(person_id=ep.pk)
        EntrevistaDeudaActual.objects.get_or_create(person_id=ep.pk,tipo="Otro")
        EntrevistaDireccion.objects.get_or_create(persona_id=ep.pk)
        EntrevistaDistribucionDimensiones.objects.get_or_create(person_id=ep.pk)
        EntrevistaInfoPersonal.objects.get_or_create(persona_id=ep.pk)
        EntrevistaLicencia.objects.get_or_create(persona_id=ep.pk)
        EntrevistaOrigen.objects.get_or_create(persona_id=ep.pk)
        EntrevistaOtroIdioma.objects.get_or_create(person_id=ep.pk)
        EntrevistaPropietarioVivienda.objects.get_or_create(person_id=ep.pk)
        EntrevistaSalud.objects.get_or_create(persona_id=ep.pk)
        EntrevistaSituacionVivienda.objects.get_or_create(person_id=ep.pk)
        EntrevistaTipoInmueble.objects.get_or_create(person_id=ep.pk)
        EntrevistaCita.objects.get_or_create(investigacion_id=self.investigacion_id)

        EntrevistaCaractaristicasVivienda.objects.get_or_create(person_id=ep.pk)
        EntrevistaInvestigacion.objects.get_or_create(investigacion_id=self.investigacion_id, agente_id=investigacion.agente.pk, persona_id=ep.pk)
       
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="acta_nacimiento")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk , tipo="acta_matrimonio")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk , tipo="comprobante_domicilio")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="id_oficial")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="comprobante_nss")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="curp")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="cartilla_smn")
        EntrevistaDocumentoCotejado.objects.get_or_create(person_id=ep.pk, tipo="ultimo_grado_estudio")
       
        EntrevistaAspectoHogar.objects.get_or_create(person_id=ep.pk, tipo="orden")
        EntrevistaAspectoHogar.objects.get_or_create(person_id=ep.pk, tipo="limpieza")
        EntrevistaAspectoHogar.objects.get_or_create(person_id=ep.pk, tipo="conservacion")

        EntrevistaAspectoCandidato.objects.get_or_create(person_id=ep.pk, tipo="disponibilidad")
        EntrevistaAspectoCandidato.objects.get_or_create(person_id=ep.pk, tipo="puntualidad")
        EntrevistaAspectoCandidato.objects.get_or_create(person_id=ep.pk, tipo="apariencia_fisica")
        EntrevistaAspectoCandidato.objects.get_or_create(person_id=ep.pk, tipo="colaboracion")
        EntrevistaAspectoCandidato.objects.get_or_create(person_id=ep.pk, tipo="actitud")
        
        EntrevistaBienesRaices.objects.get_or_create(person_id=ep.pk,tipo_inmueble="Otro")

        EntrevistaAutomovil.objects.get_or_create(person_id=ep.pk, valor_comercial="", marca="", liquidacion="", modelo_ano="")
        EntrevistaAutomovil.objects.get_or_create(person_id=ep.pk, valor_comercial="", marca="N/A", liquidacion="", modelo_ano="")

        EntrevistaCuentaDebito.objects.get_or_create(person_id=ep.pk,institucion="", saldo_mensual="", antiguedad="", ahorro="")
        EntrevistaCuentaDebito.objects.get_or_create(person_id=ep.pk,institucion="N/A", saldo_mensual="", antiguedad="", ahorro="")
    
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="investigado", tipo="ingreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="conyuge", tipo="ingreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="padres", tipo="ingreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="hermanos", tipo="ingreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="otros", tipo="ingreso")

        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="impuestos", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="vestimenta", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="gastos_automovil", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="transporte_publico", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="alimentacion", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="educacion", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="medico", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="diversos", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="servicios", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="serv_domestico", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="seguros", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="deuda1", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="deuda2", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="otros", tipo="egreso")
        EntrevistaEconomica.objects.get_or_create(person_id=ep.pk, monto="", concepto="total", tipo="egreso")
        
      
        EntrevistaGradoEscolaridad.objects.get_or_create(person_id=ep.pk, grado="primaria", anos="", institucion="", ciudad="", certificado="")
        EntrevistaGradoEscolaridad.objects.get_or_create(person_id=ep.pk, grado="secundaria", anos="", institucion="", ciudad="", certificado="")
        EntrevistaGradoEscolaridad.objects.get_or_create(person_id=ep.pk, grado="preparatoria", anos="", institucion="", ciudad="", certificado="")
        EntrevistaGradoEscolaridad.objects.get_or_create(person_id=ep.pk, grado="profesional", anos="", institucion="", ciudad="", certificado="")
        EntrevistaGradoEscolaridad.objects.get_or_create(person_id=ep.pk, grado="otro_grado", anos="", institucion="", ciudad="", certificado="" )

        EntrevistaHistorialEnEmpresa.objects.get_or_create(persona_id=ep.pk, categoria="trabajo",)
        EntrevistaHistorialEnEmpresa.objects.get_or_create(persona_id=ep.pk, categoria="familiar",)
    
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="padre", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="madre", residencia="",  nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="hermano", residencia="",  nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="hermano", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="hermano", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="hermano", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="pareja", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="hijo", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="hijo", residencia="",nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="hijo", residencia="",  nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="hijo", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre="", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre=" N/A", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk,edad="", empresa="", ocupacion="", tipo="otro", residencia="",  nombre="  N/A", telefono="")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre="", telefono="", parentesco="", category="2")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre="", telefono="", parentesco="ESPECIFICAR",  category="2")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre="", telefono="", parentesco=" ESPECIFICAR",  category="2")
        EntrevistaMiembroMarcoFamiliar.objects.get_or_create(person_id=ep.pk, edad="", empresa="", ocupacion="", tipo="otro", residencia="", nombre="", telefono="", parentesco="  ESPECIFICAR",  category="2")

        EntrevistaPrestacionVivienda.objects.get_or_create(persona_id=ep.pk, uso="", fecha_tramite="", categoria_viv="infonavit", activo="", numero_credito="")
        EntrevistaPrestacionVivienda.objects.get_or_create(persona_id=ep.pk,  uso="", fecha_tramite="", categoria_viv="fonacot", activo="", numero_credito="")
            
        EntrevistaReferencia.objects.get_or_create(person_id=ep.pk, parentesco="", tiempo_conocido="", lugares_labor_evaluado="", opinion="", nombre="", ocupacion="", telefono="", domicilio="")
        EntrevistaReferencia.objects.get_or_create(person_id=ep.pk, parentesco="", tiempo_conocido="", lugares_labor_evaluado="",  opinion="", nombre="*", ocupacion="", telefono="", domicilio="")
       
        EntrevistaSeguro.objects.get_or_create(person_id=ep.pk, empresa="", vigencia="", tipo="", forma_pago="")
        EntrevistaSeguro.objects.get_or_create(person_id=ep.pk, empresa="N/A", vigencia="", tipo="", forma_pago="")
        
        EntrevistaTarjetaCreditoComercial.objects.get_or_create(person_id=ep.pk, institucion="", saldo_actual="", pago_minimo="", limite_credito="")
        EntrevistaTarjetaCreditoComercial.objects.get_or_create(person_id=ep.pk, institucion="N/A", saldo_actual="", pago_minimo="", limite_credito="")

        EntrevistaTelefono.objects.get_or_create(persona_id=ep.pk, categoria="casa", parentesco="", numero="")
        EntrevistaTelefono.objects.get_or_create(persona_id=ep.pk, categoria="movil", parentesco="", numero="")
        EntrevistaTelefono.objects.get_or_create(persona_id=ep.pk, categoria="recado", parentesco="", numero="")
        EntrevistaTelefono.objects.get_or_create(persona_id=ep.pk, categoria="otro", parentesco="", numero="")

        print("EntrevistaPersonaService se ha generado" )

        return True
