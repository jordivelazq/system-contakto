from django import forms

from ..models import ClienteSolicitudCandidato


class  ClienteSolicitudCandidatoForm(forms.ModelForm):

    class Meta:
        model = ClienteSolicitudCandidato
        fields = ('nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'sucursal',
              'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud', 'telefono_casa', 'telefono_movil', 'direccion_fiscal')
       