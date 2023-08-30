from rest_framework import serializers

from .models import Investigacion
from app.persona.models import Persona, File
from app.compania.models import Compania, Sucursales, Contacto

from django.contrib.auth.models import User


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


class InvestigacionSerializer(serializers.ModelSerializer):

    agente = UserSerializer(read_only=True)
    candidato = PersonaSerializer(read_only=True)
    compania = CompaniaSerializer(read_only=True)
    sucursal = SucursalesSerializer(read_only=True)
    contacto = ContactoSerializer(read_only=True)
    file = FileSerializer(read_only=True)

    class Meta:
        model = Investigacion
        fields = '__all__'