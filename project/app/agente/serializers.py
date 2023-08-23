from django.contrib.auth.models import User
from rest_framework import serializers

from .models import GestorInfo


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class GestorInfoSerializer(serializers.ModelSerializer):

    estatus = ChoiceField(choices=GestorInfo.ESTATUS)
    tipo_pago = ChoiceField(choices=GestorInfo.TIPO_PAGO)
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = GestorInfo
        fields = ('__all__')
