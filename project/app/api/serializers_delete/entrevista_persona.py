from rest_framework import serializers

from app.compania.models import Compania, Contacto, Sucursales

# from app.solicitud.models import Servicio, AdjuntoSolicitud

from app.persona.models import Persona

# No existe la aplicacion de Servicio
# class ServicioSerializer(serializers.ModelSerializer):
#     costo = serializers.SerializerMethodField()

#     def get_costo(self, obj):
#         return "${:,.2f}".format(obj.costo)

#     class Meta:
#         model = Servicio
#         fields = '__all__'


class CompaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compania
        fields = '__all__'


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'


class SucursalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursales
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


# class AdjuntoSolicitudSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdjuntoSolicitud
#         fields = '__all__'
