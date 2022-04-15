from django.contrib.auth.models import User
from rest_framework import serializers

from app.compania.models import Compania, Sucursales
from app.investigacion.models import Investigacion
from app.adjuntos.models import Adjuntos
from app.entrevista.models import EntrevistaPersona, EntrevistaSalud, EntrevistaAcademica, EntrevistaDireccion, \
    EntrevistaTelefono, EntrevistaReferencia, EntrevistaSeguro, EntrevistaEconomica, \
    EntrevistaInfoPersonal, EntrevistaPrestacionVivienda, EntrevistaLicencia, EntrevistaOrigen, \
    EntrevistaHistorialEnEmpresa, EntrevistaActividadesHabitos
from app.persona.models import Telefono, Direccion, Persona


class AdjuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjuntos
        fields = '__all__'


class EntrevistaSeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaSeguro
        fields = '__all__'


class EntrevistaEconomicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaEconomica
        fields = '__all__'


class EntrevistaInfoPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaInfoPersonal
        fields = '__all__'


class EntrevistaSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaSalud
        fields = '__all__'


class EntrevistaAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaAcademica
        fields = '__all__'


class EntrevistaDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaDireccion
        fields = '__all__'


class EntrevistaTelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaTelefono
        fields = '__all__'


class EntrevistaReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaReferencia
        fields = '__all__'


class EntrevistaPrestacionViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaPrestacionVivienda
        fields = '__all__'


class EntrevistaLicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaLicencia
        fields = '__all__'


class EntrevistaOrigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaOrigen
        fields = '__all__'


class EntrevistaHistorialEnEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaHistorialEnEmpresa
        fields = '__all__'


class EntrevistaActividadesHabitosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaActividadesHabitos

        fields = '__all__'


# ENTREVISTA PERSONA

class EntrevistaPersonaSerializer(serializers.ModelSerializer):
    entrevista_seguro = serializers.SerializerMethodField()
    entrevista_economica = serializers.SerializerMethodField()
    entrevista_referencia = serializers.SerializerMethodField()
    entrevista_salud = serializers.SerializerMethodField()
    entrevista_academica = serializers.SerializerMethodField()
    entrevista_direccion = serializers.SerializerMethodField()
    entrevista_telefono = serializers.SerializerMethodField()
    entrevista_presentacion_vivienda = serializers.SerializerMethodField()
    entrevista_licencia = serializers.SerializerMethodField()
    entrevista_origen = serializers.SerializerMethodField()
    entrevista_informacion_personal = serializers.SerializerMethodField()
    entrevista_historial_en_empresa = serializers.SerializerMethodField()
    entrevista_actividades_habitos = serializers.SerializerMethodField()

    def get_entrevista_seguro(self, obj):
        queryset = EntrevistaSeguro.objects.filter(person_id=obj.pk)
        serializer = EntrevistaSeguroSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_economica(self, obj):
        queryset = EntrevistaEconomica.objects.filter(person_id=obj.pk)
        serializer = EntrevistaEconomicaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_referencia(self, obj):
        queryset = EntrevistaReferencia.objects.filter(person_id=obj.pk)
        serializer = EntrevistaReferenciaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_salud(self, obj):
        queryset = EntrevistaSalud.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaSaludSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_academica(self, obj):
        queryset = EntrevistaAcademica.objects.filter(person_id=obj.pk)
        serializer = EntrevistaAcademicaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_direccion(self, obj):
        queryset = EntrevistaDireccion.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaDireccionSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_telefono(self, obj):
        queryset = EntrevistaTelefono.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaTelefonoSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_presentacion_vivienda(self, obj):
        queryset = EntrevistaPrestacionVivienda.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaPrestacionViviendaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_licencia(self, obj):
        queryset = EntrevistaLicencia.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaLicenciaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_origen(self, obj):
        queryset = EntrevistaOrigen.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaOrigenSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_informacion_personal(self, obj):
        queryset = EntrevistaInfoPersonal.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaInfoPersonalSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_historial_en_empresa(self, obj):
        queryset = EntrevistaHistorialEnEmpresa.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaHistorialEnEmpresaSerializer(queryset, many=True)
        return serializer.data

    def get_entrevista_actividades_habitos(self, obj):
        queryset = EntrevistaActividadesHabitos.objects.filter(persona_id=obj.pk)
        serializer = EntrevistaActividadesHabitosSerializer(queryset, many=True)
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
