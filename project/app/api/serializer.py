from app.adjuntos.models import Adjuntos
from app.compania.models import Compania, Sucursales
from app.entrevista.models import (EntrevistaAcademica,
                                   EntrevistaActividadesHabitos,
                                   EntrevistaAspectoCandidato,
                                   EntrevistaAspectoHogar, EntrevistaAutomovil,
                                   EntrevistaBienesRaices,
                                   EntrevistaCaractaristicasVivienda,
                                   EntrevistaCuentaDebito,
                                   EntrevistaDeudaActual, EntrevistaDireccion,
                                   EntrevistaDistribucionDimensiones,
                                   EntrevistaDocumentoCotejado,
                                   EntrevistaEconomica,
                                   EntrevistaGradoEscolaridad,
                                   EntrevistaHistorialEnEmpresa,
                                   EntrevistaInfoPersonal, EntrevistaLicencia,
                                   EntrevistaMiembroMarcoFamiliar,
                                   EntrevistaOrigen, EntrevistaOtroIdioma,
                                   EntrevistaPersona,
                                   EntrevistaPropietarioVivienda,
                                   EntrevistaReferencia, EntrevistaSeguro,
                                   EntrevistaSituacionVivienda,
                                   EntrevistaSalud, EntrevistaPrestacionVivienda,
                                   EntrevistaTarjetaCreditoComercial,
                                   EntrevistaTelefono, EntrevistaTipoInmueble)
from app.investigacion.models import Investigacion
from app.persona.models import Direccion, Persona, Telefono
from django.contrib.auth.models import User
from rest_framework import serializers


class AdjuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjuntos
        fields = '__all__'


class EntrevistaAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaAcademica
        fields = '__all__'


class EntrevistaActividadesHabitosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaActividadesHabitos

        fields = '__all__'


class EntrevistaAspectoCandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaAspectoCandidato
        fields = '__all__'


class EntrevistaAspectoHogarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaAspectoHogar
        fields = '__all__'


class EntrevistaAutomovilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaAutomovil
        fields = '__all__'


class EntrevistaBienesRaicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaBienesRaices
        fields = '__all__'

class EntrevistaCaracteristicasViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaCaractaristicasVivienda
        fields = '__all__'

class EntrevistaCuentaDebitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaCuentaDebito
        fields = '__all__'


class EntrevistaDeudaActualSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaDeudaActual
        fields = '__all__'


class EntrevistaDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaDireccion
        fields = '__all__'


class EntrevistaDistribucionDimensionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaDistribucionDimensiones
        fields = '__all__'


class EntrevistaDocumentoCotejadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaDocumentoCotejado
        fields = '__all__'


class EntrevistaEconomicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaEconomica
        fields = '__all__'


class EntrevistaGradoEscolaridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaGradoEscolaridad
        fields = '__all__'


class EntrevistaHistorialEnEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaHistorialEnEmpresa
        fields = '__all__'


class EntrevistaInfoPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaInfoPersonal
        fields = '__all__'


class EntrevistaLicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaLicencia
        fields = '__all__'


class EntrevistaMiembroMarcoFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaMiembroMarcoFamiliar
        fields = '__all__'


class EntrevistaOrigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaOrigen
        fields = '__all__'


class EntrevistaOtroIdiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaOtroIdioma
        fields = '__all__'


class EntrevistaPropietarioViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaPropietarioVivienda
        fields = '__all__'


class EntrevistaReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaReferencia
        fields = '__all__'


class EntrevistaSeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaSeguro
        fields = '__all__'


class EntrevistaSituacionViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaSituacionVivienda
        fields = '__all__'


class EntrevistaSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaSalud
        fields = '__all__'


class EntrevistaPrestacionViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaPrestacionVivienda
        fields = '__all__'


class EntrevistaTarjetaCreditoComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaTarjetaCreditoComercial
        fields = '__all__'


class EntrevistaTelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaTelefono
        fields = '__all__'


class EntrevistaTipoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaTipoInmueble
        fields = '__all__'


# ENTREVISTA PERSONA

class EntrevistaPersonaSerializer(serializers.ModelSerializer):
    entrevista_academica = serializers.SerializerMethodField()
    entrevista_actividades_habitos = serializers.SerializerMethodField()
    entrevista_aspecto_candidato = serializers.SerializerMethodField()
    entrevista_aspecto_hogar = serializers.SerializerMethodField()
    entrevista_automovil = serializers.SerializerMethodField()
    entrevista_bienes_raices = serializers.SerializerMethodField()
    entrevista_caracteristicas_vivienda = serializers.SerializerMethodField()
    entrevista_cuenta_debito = serializers.SerializerMethodField()
    entrevista_deuda_actual = serializers.SerializerMethodField()
    entrevista_direccion = serializers.SerializerMethodField()
    entrevista_distribucion_dimensiones = serializers.SerializerMethodField()
    entrevista_documento_cotejado = serializers.SerializerMethodField()
    entrevista_economica = serializers.SerializerMethodField()
    entrevista_grado_escolaridad = serializers.SerializerMethodField()
    entrevista_historial_en_empresa = serializers.SerializerMethodField()
    entrevista_informacion_personal = serializers.SerializerMethodField()
    entrevista_licencia = serializers.SerializerMethodField()
    entrevista_miembro_marco_familiar = serializers.SerializerMethodField()
    entrevista_origen = serializers.SerializerMethodField()
    entrevista_otro_idioma = serializers.SerializerMethodField()
    entrevista_propietario_vivienda = serializers.SerializerMethodField()
    entrevista_referencia = serializers.SerializerMethodField()
    entrevista_seguro = serializers.SerializerMethodField()
    entrevista_seguro = serializers.SerializerMethodField()
    entrevista_situacion_vivienda = serializers.SerializerMethodField()
    entrevista_salud = serializers.SerializerMethodField()
    entrevista_presentacion_vivienda = serializers.SerializerMethodField()
    entrevista_tarjeta_credito_comercial = serializers.SerializerMethodField()
    entrevista_telefono = serializers.SerializerMethodField()
    entrevista_tipo_inmueble = serializers.SerializerMethodField()

    def get_entrevista_academica(self, obj):
        queryset = EntrevistaAcademica.objects.filter(person_id=obj.pk)
        serializer = EntrevistaAcademicaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_actividades_habitos(self, obj):
        queryset = EntrevistaActividadesHabitos.objects.filter(
            persona_id=obj.pk)
        serializer = EntrevistaActividadesHabitosSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_aspecto_candidato(self, obj):
        queryset = EntrevistaAspectoCandidato.objects.filter(person_id=obj.pk)
        serializer = EntrevistaAspectoCandidatoSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_automovil(self, obj):
        queryset = EntrevistaAutomovil.objects.filter(person_id=obj.pk)
        serializer = EntrevistaAutomovilSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_aspecto_hogar(self, obj):
        queryset = EntrevistaAspectoHogar.objects.filter(person_id=obj.pk)
        serializer = EntrevistaAspectoHogarSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_bienes_raices(self, obj):
        queryset = EntrevistaBienesRaices.objects.filter(person_id=obj.pk)
        serializer = EntrevistaBienesRaicesSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_caracteristicas_vivienda(self, obj):
        queryset = EntrevistaCaractaristicasVivienda.objects.filter(person_id=obj.pk)
        serializer = EntrevistaCaracteristicasViviendaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_cuenta_debito(self, obj):
        queryset = EntrevistaCuentaDebito.objects.filter(person_id=obj.pk)
        serializer = EntrevistaCuentaDebitoSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_deuda_actual(self, obj):
        queryset = EntrevistaDeudaActual.objects.filter(person_id=obj.pk)
        serializer = EntrevistaDeudaActualSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_direccion(self, obj):
        queryset = EntrevistaDireccion.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaDireccionSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_distribucion_dimensiones(self, obj):
        queryset = EntrevistaDistribucionDimensiones.objects.filter(
            person_id=obj.pk)
        serializer = EntrevistaDistribucionDimensionesSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_documento_cotejado(self, obj):
        queryset = EntrevistaDocumentoCotejado.objects.filter(person_id=obj.pk)
        serializer = EntrevistaDocumentoCotejadoSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_economica(self, obj):
        queryset = EntrevistaEconomica.objects.filter(person_id=obj.pk)
        serializer = EntrevistaEconomicaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_grado_escolaridad(self, obj):
        queryset = EntrevistaGradoEscolaridad.objects.filter(person_id=obj.pk)
        serializer = EntrevistaGradoEscolaridadSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_historial_en_empresa(self, obj):
        queryset = EntrevistaHistorialEnEmpresa.objects.filter(
            persona_id=obj.pk)
        serializer = EntrevistaHistorialEnEmpresaSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_informacion_personal(self, obj):
        queryset = EntrevistaInfoPersonal.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaInfoPersonalSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_licencia(self, obj):
        queryset = EntrevistaLicencia.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaLicenciaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_miembro_marco_familiar(self, obj):
        queryset = EntrevistaMiembroMarcoFamiliar.objects.filter(
            person_id=obj.pk)
        serializer = EntrevistaMiembroMarcoFamiliarSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_origen(self, obj):
        queryset = EntrevistaOrigen.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaOrigenSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_otro_idioma(self, obj):
        queryset = EntrevistaOtroIdioma.objects.filter(person_id=obj.pk)
        serializer = EntrevistaOtroIdiomaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_propietario_vivienda(self, obj):
        queryset = EntrevistaPropietarioVivienda.objects.filter(
            person_id=obj.pk)
        serializer = EntrevistaPropietarioViviendaSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_referencia(self, obj):
        queryset = EntrevistaReferencia.objects.filter(person_id=obj.pk)
        serializer = EntrevistaReferenciaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_seguro(self, obj):
        queryset = EntrevistaSeguro.objects.filter(person_id=obj.pk)
        serializer = EntrevistaSeguroSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_situacion_vivienda(self, obj):
        queryset = EntrevistaSituacionVivienda.objects.filter(
            person_id=obj.pk)
        serializer = EntrevistaSituacionViviendaSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_salud(self, obj):
        queryset = EntrevistaSalud.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaSaludSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_presentacion_vivienda(self, obj):
        queryset = EntrevistaPrestacionVivienda.objects.filter(
            persona_id=obj.pk)
        serializer = EntrevistaPrestacionViviendaSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_tarjeta_credito_comercial(self, obj):
        queryset = EntrevistaTarjetaCreditoComercial.objects.filter(
            person_id=obj.pk)
        serializer = EntrevistaTarjetaCreditoComercialSerializer(
            queryset, many=True)
        return serializer.data

    def get_entrevista_telefono(self, obj):
        queryset = EntrevistaTelefono.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaTelefonoSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_tipo_inmueble(self, obj):
        queryset = EntrevistaTipoInmueble.objects.filter(person_id=obj.pk)
        serializer = EntrevistaTipoInmuebleSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = EntrevistaPersona
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = '__all__'


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'


class CompaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compania
        fields = '__all__'


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursales
        fields = '__all__'


class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class InvestigacionSerializer(serializers.ModelSerializer):
    adjuntos = serializers.SerializerMethodField()
    entrevista_persona = serializers.SerializerMethodField()
    telefono = serializers.SerializerMethodField()
    direccion = serializers.SerializerMethodField()

    def get_adjuntos(self, obj):
        queryset = Adjuntos.objects.filter(investigacion_id=obj.pk)
        serializer = AdjuntosSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_persona(self, obj):
        queryset = EntrevistaPersona.objects.filter(investigacion_id=obj.pk)
        serializer = EntrevistaPersonaSerializer(queryset, many=True)
        return serializer.data

    def get_telefono(self, obj):
        queryset = Telefono.objects.filter(persona_id=obj.candidato_id)
        serializer = TelefonoSerializer(queryset, many=True)
        return serializer.data

    def get_direccion(self, obj):
        queryset = Direccion.objects.filter(persona_id=obj.candidato_id)
        serializer = DireccionSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Investigacion
        fields = '__all__'


class InvestigacionListSerializer(serializers.ModelSerializer):
    telefono = serializers.SerializerMethodField()
    direccion = serializers.SerializerMethodField()
    compania = CompaniaSerializer()
    sucursal = SucursalSerializer()
    agente = AgenteSerializer()
    candidato = PersonaSerializer()

    def get_telefono(self, obj):
        queryset = Telefono.objects.filter(persona_id=obj.candidato_id)
        serializer = TelefonoSerializer(queryset, many=True)
        return serializer.data

    def get_direccion(self, obj):
        queryset = Direccion.objects.filter(persona_id=obj.candidato_id)
        serializer = DireccionSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Investigacion
        fields = '__all__'
