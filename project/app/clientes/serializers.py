from rest_framework import serializers

from .models import ClienteUser
from app.compania.models import Compania


class CompaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compania
        fields = ('id', 'nombre')


class ClienteUserSerializer(serializers.ModelSerializer):

    compania = CompaniaSerializer(read_only=True)

    class Meta:
        model = ClienteUser
        fields = '__all__'