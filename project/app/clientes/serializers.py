from rest_framework import serializers

from .models import ClienteUser, ClienteSolicitud
from app.compania.models import Compania

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class User:
        model = ClienteSolicitud
        fields = ('id', 'username', 'first_name', 'last_name', 'email')



class ClienteSolicitudSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = ClienteSolicitud
        fields = '__all__'


class CompaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compania
        fields = ('id', 'nombre')


class ClienteUserSerializer(serializers.ModelSerializer):

    compania = CompaniaSerializer(read_only=True)

    class Meta:
        model = ClienteUser
        fields = '__all__'