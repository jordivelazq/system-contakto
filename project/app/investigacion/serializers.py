from rest_framework import serializers

from .models import Investigacion, Psicometrico, GestorInvestigacion, GestorInfo, GestorInvestigacionPago
from app.persona.models import Persona, File
from app.compania.models import Compania, Sucursales, Contacto
from app.clientes.models import ClienteTipoInvestigacion

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class CompaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compania
        fields = "__all__"


class SucursalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursales
        fields = "__all__"


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = "__all__"


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ClienteTipoInvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteTipoInvestigacion
        fields = '__all__'


class PsicometricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psicometrico
        fields = '__all__'


class InvestigacionSerializer(serializers.ModelSerializer):
    agente = UserSerializer(read_only=True)
    ejecutivo_visitas = UserSerializer(read_only=True)
    candidato = PersonaSerializer(read_only=True)
    compania = CompaniaSerializer(read_only=True)
    sucursal = SucursalesSerializer(read_only=True)
    contacto = ContactoSerializer(read_only=True)
    tipo_investigacion = serializers.SerializerMethodField()
    file = FileSerializer(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    agente_name = serializers.SerializerMethodField()
    cita = serializers.SerializerMethodField()

    class Meta:
        model = Investigacion
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status_display()

    def get_tipo_investigacion(self, obj):
        return obj.tipo_investigacion.last().tipo_investigacion if obj.tipo_investigacion.last() else 'N/A'

    def get_agente_name(self, obj):
        return obj.agente.username if obj.agente else 'No asignado'

    def get_cita(self, obj):
        cita = obj.entrevistacita_set.first()
        if cita.fecha_entrevista and cita.hora_entrevista:
            return '{} {} / {}'.format(cita.fecha_entrevista, cita.hora_entrevista, cita.entrevistador)
        return 'No asignado'


class GestorInfoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    # usuario = serializers.StringRelatedField(many=True)

    class Meta:
        model = GestorInfo
        # fields = ['usuario']
        fields = '__all__'


class GestorInvestigacionSerializer(serializers.ModelSerializer):
    # investigacion = InvestigacionSerializer(read_only=True)
    gestor = GestorInfoSerializer(read_only=True)
    # gestor = serializers.ReadOnlyField(source='gestorinfo.usuario')
    # gestor = serializers.RelatedField(many=True, read_only=True)
    # total_inv = serializers.IntegerField()
    gcount = serializers.IntegerField()

    # count_investigaciones = serializers.SerializerMethodField(read_only=True)

    # investigacion = serializers.StringRelatedField(many=True)

    class Meta:
        model = GestorInvestigacion
        fields = ['gestor', 'gcount']
        # fields = '__all__'


class GestorInvestigacionPagoSerializer(serializers.ModelSerializer):
    gestor = GestorInfoSerializer(read_only=True)

    class Meta:
        model = GestorInvestigacionPago
        fields = '__all__'
