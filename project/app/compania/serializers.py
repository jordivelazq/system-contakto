from rest_framework import serializers

from .models import Compania
from app.compania.models import Compania
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CompaniaSerializer(serializers.ModelSerializer):

    coordinador_ejecutivos = UserSerializer(read_only=True)

    class Meta:
        model = Compania
        fields = '__all__'