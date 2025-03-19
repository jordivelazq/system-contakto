from django import forms

from ..models import ClienteSolicitudCandidato


class  ClienteSolicitudCandidatoForm(forms.ModelForm):
    archivo_otros = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ClienteSolicitudCandidato
        fields = ('nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'sucursal',
              'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud', 'archivo_otros', 'telefono_casa', 'telefono_movil', 'direccion_fiscal')
       