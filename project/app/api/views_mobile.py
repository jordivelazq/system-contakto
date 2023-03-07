import uuid

from app.adjuntos.models import Adjuntos
from app.agente.models import GestorInfo
from app.api.serializer import (AdjuntosSerializer,
                                InvestigacionListSerializer,
                                InvestigacionSerializer)
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.entrevista.models import (EntrevistaAcademica,
                                   EntrevistaActividadesHabitos,
                                   EntrevistaAspectoCandidato,
                                   EntrevistaAspectoHogar, EntrevistaAutomovil,
                                   EntrevistaBienesRaices,
                                   EntrevistaCaractaristicasVivienda,
                                   EntrevistaCuentaDebito,
                                   EntrevistaDeudaActual, EntrevistaDireccion,
                                   EntrevistaDistribucionDimensiones,
                                   EntrevistaDocumentoCotejado,
                                   EntrevistaEconomica,
                                   EntrevistaGradoEscolaridad,
                                   EntrevistaHistorialEnEmpresa,
                                   EntrevistaInfoPersonal, EntrevistaLicencia,
                                   EntrevistaMiembroMarcoFamiliar,
                                   EntrevistaOrigen, EntrevistaOtroIdioma,
                                   EntrevistaPersona,
                                   EntrevistaPrestacionVivienda,
                                   EntrevistaPropietarioVivienda,
                                   EntrevistaReferencia, EntrevistaSalud,
                                   EntrevistaSeguro,
                                   EntrevistaSituacionVivienda,
                                   EntrevistaTarjetaCreditoComercial,
                                   EntrevistaTelefono, EntrevistaTipoInmueble)
from app.investigacion.models import Investigacion
from app.persona.models import DatosGenerales
from django.conf import settings
from oauth2_provider.contrib.rest_framework import (OAuth2Authentication,
                                                    TokenHasReadWriteScope,
                                                    )
from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import (EntrevistaAcademicaSerializer,
                         EntrevistaActividadesHabitosSerializer,
                         EntrevistaAspectoCandidatoSerializer,
                         EntrevistaAspectoHogarSerializer,
                         EntrevistaAutomovilSerializer,
                         EntrevistaBienesRaicesSerializer,
                         EntrevistaCaracteristicasViviendaSerializer,
                         EntrevistaCuentaDebitoSerializer,
                         EntrevistaDeudaActualSerializer,
                         EntrevistaDireccionSerializer,
                         EntrevistaDistribucionDimensionesSerializer,
                         EntrevistaDocumentoCotejadoSerializer,
                         EntrevistaEconomicaSerializer,
                         EntrevistaGradoEscolaridadSerializer,
                         EntrevistaHistorialEnEmpresaSerializer,
                         EntrevistaInfoPersonalSerializer,
                         EntrevistaLicenciaSerializer,
                         EntrevistaMiembroMarcoFamiliarSerializer,
                         EntrevistaOrigenSerializer,
                         EntrevistaOtroIdiomaSerializer,
                         EntrevistaPersonaSerializer,
                         EntrevistaPrestacionViviendaSerializer,
                         EntrevistaPropietarioViviendaSerializer,
                         EntrevistaReferenciaSerializer,
                         EntrevistaSaludSerializer, EntrevistaSeguroSerializer,
                         EntrevistaSituacionViviendaSerializer,
                         EntrevistaTarjetaCreditoComercialSerializer,
                         EntrevistaTelefonoSerializer,
                         EntrevistaTipoInmuebleSerializer)


class AsignacionInvestigacionApiView(APIView):
    model = Investigacion
    serializer_class = InvestigacionSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]

    # def get_queryset(self):
    #     # return Investigacion.objects.filter(pk=self.kwargs.get('pk'))
    #     return Investigacion.objects.filter(pk=100)

    def get(self, request, *args, **kwargs):
        data = {'message': 'Petición no procesada', 'error': 1}
        try:
            gestor = GestorInfo.objects.get(usuario=self.request.user)
            queryset = Investigacion.objects.filter(
                gestorinvestigacion__gestor=gestor, gestorinvestigacion__estatus=2)
            serializer = InvestigacionListSerializer(queryset, many=True)
            data = {'message': 'Datos correctos',
                    'error': 0, 'data': serializer.data}
        except Exception as e:
            data = {'message': 'Ha ocurrido un error interno. {}'.format(
                e.args), 'error': 2}
        return Response(data=data)
    
    # def get(self, request, *args, **kwargs):
    #     data = {'message': 'Petición no procesada', 'error': 1}
    #     try:
    #         gestor = GestorInfo.objects.get(usuario=self.request.user)
    #     except GestorInfo.DoesNotExist:
    #         data = {'message': 'Petición no procesada', 'error': 1}
    #         return Response(data=data)    
    #     try:
    #         queryset = Investigacion.objects.filter(
    #             gestorinvestigacion__gestor=gestor, gestorinvestigacion__estatus=2)
    #         serializer = InvestigacionListSerializer(queryset, many=True)
    #         data = {'message': 'Datos correctos',
    #                 'error': 0, 'data': serializer.data}
    #     except Exception as e:
    #         data = {'message': 'Ha ocurrido un error interno. {}'.format(
    #             e.args), 'error': 2}
    #     return Response(data=data)


class InvestigacionDetailApiView(ListAPIView):
    model = Investigacion
    serializer_class = InvestigacionSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def get_queryset(self):
        return Investigacion.objects.filter(pk=self.kwargs.get('pk'))


class InvestigacionUploadImageApiView(APIView):
    parser_class = (FileUploadParser,)
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('inv'):
            queryset = Adjuntos.objects.filter(
                investigacion_id=self.request.GET.get('inv'))
            serializer = AdjuntosSerializer(queryset, many=True)
            return Response(data={'error': 0, 'message': 'Adjuntos de investigación', 'data': serializer.data},
                            status=200)
        return Response(data={'error': 1, 'message': 'No se ha completado el proceso. Inténtelo nuevamente.'},
                        status=401)

    def put(self, request, format=None):
        investigacion_id = self.request.GET.get('inv')
        column_no = self.request.GET.get('column_no')
        if 'file' not in request.data:
            return Response(
                data={
                    'error': 4, 'message': 'Archivo no encontrado, inténtelo nuevamente usando datos correctos.'},
                status=404)
        f = request.data['file']
        ext = f.name.split('.')
        ext = ext[len(ext) - 1]
        f.name = '{}.{}'.format(uuid.uuid4(), ext)
        destination = open(settings.MEDIA_ROOT + '/' + f.name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        if investigacion_id and column_no:
            try:
                adjunto = Adjuntos.objects.filter(
                    investigacion_id=investigacion_id)
                if not adjunto:
                    Adjuntos.objects.create(investigacion_id=investigacion_id)
                    adjunto = Adjuntos.objects.filter(
                        investigacion_id=investigacion_id)
                # adj2='1. Foto de perfil del candidato'
                if column_no == '2':
                    adjunto.update(adj2=f)
                # adj3='2.a Interior derecho'
                if column_no == '3':
                    adjunto.update(adj3=f)
                # adj4='2.b Interior izquierdo'
                if column_no == '4':
                    adjunto.update(adj4=f)
                # adj5='2.c Exterior derecho'
                if column_no == '5':
                    adjunto.update(adj5=f)
                # adj6='2.d Exterior izquierdo'
                if column_no == '6':
                    adjunto.update(adj6=f)
                # adj9='2.e Frente'
                if column_no == '9':
                    adjunto.update(adj9=f)
                # adj10='3. Gestor Entrevistador'
                if column_no == '10':
                    adjunto.update(adj10=f)
                # adj13='4. Croquis'
                if column_no == '13':
                    adjunto.update(adj13=f)
                # adj11='5. Aviso Privacidad'
                if column_no == '11':
                    adjunto.update(adj11=f)
                # adj12='6. Constancia'
                if column_no == '12':
                    adjunto.update(adj12=f)
                # adj14='7.a Identificación con fotografia'
                if column_no == '14':
                    adjunto.update(adj14=f)
                # adj22='7.b Identificación con fotografia'
                if column_no == '22':
                    adjunto.update(adj22=f)
                # adj23='7.c Identificación con fotografia'
                if column_no == '23':
                    adjunto.update(adj23=f)
                # adj24='7.d Identificación con fotografia'
                if column_no == '24':
                    adjunto.update(adj24=f)
                # adj17='8. Acta de nacimiento'

                if column_no == '17':
                    adjunto.update(adj17=f)
                # adj16='9. Comprobante de domicilio'

                if column_no == '16':
                    adjunto.update(adj16=f)
                # adj8='10.a Semanas Cotizadas'

                if column_no == '8':
                    adjunto.update(adj8=f)
                # adj25='10.b Semanas Cotizadas'

                if column_no == '25':
                    adjunto.update(adj25=f)
                # adj26='10.c Semanas Cotizadas'

                if column_no == '26':
                    adjunto.update(adj26=f)
                # adj27='10.d Semanas Cotizadas'

                if column_no == '27':
                    adjunto.update(adj27=f)
                # adj28='10.e Semanas Cotizadas'

                if column_no == '28':
                    adjunto.update(adj28=f)
                # adj7='11.a Validación de Demandas Laborales'

                if column_no == '7':
                    adjunto.update(adj7=f)
                # adj36='11.b Validacion web'

                if column_no == '36':
                    adjunto.update(adj36=f)
                # adj18='Carta Laboral'

                if column_no == '18':
                    adjunto.update(adj18=f)
                # adj37='Carta Laboral Extra'

                if column_no == '37':
                    adjunto.update(adj37=f)
                # adj19='Adicionales A'

                if column_no == '19':
                    adjunto.update(adj19=f)
                # adj20='Adicionales B'

                if column_no == '20':
                    adjunto.update(adj20=f)
                # adj21='Adicionales C'

                if column_no == '21':
                    adjunto.update(adj21=f)

                # adj29='Adicionales D'

                if column_no == '29':
                    adjunto.update(adj29=f)

                # adj30='Adicionales E'

                if column_no == '30':
                    adjunto.update(adj30=f)

                # adj31='Adicionales F'

                if column_no == '31':
                    adjunto.update(adj31=f)
                # adj32='Adicionales G'

                if column_no == '32':
                    adjunto.update(adj32=f)

                # adj33='Adicionales H'
                if column_no == '33':
                    adjunto.update(adj33=f)
                # adj34='Adicionales I'
                if column_no == '34':
                    adjunto.update(adj34=f)
                # adj35='Extra A'
                if column_no == '35':
                    adjunto.update(adj35=f)
                return Response(data={'error': 1, 'message': 'Foto ha sido guardada correctamente', }, status=200)
            except Exception as e:
                return Response(data={'error': 2,
                                      'message': 'No se ha encontrado el adjunto de la investigacion, inténtelo nuevamente. {}'.format(
                                          str(e))},
                                status=404)
        return Response(data={'error': 3, 'message': 'No se ha completado el proceso. Inténtelo nuevamente.'},
                        status=401)


class VerificaEntrevistaPersona(APIView):
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def post(self, request, *args, **kwargs):
        data = {'message': 'Petición no procesada', 'error': 1}
        try:
            investigacion_id = self.kwargs['investigacion_id']
            ep = EntrevistaPersonaService(investigacion_id).verifyData()
            print(ep)
            if ep:
                data = {'message': 'Datos generados',
                        'error': 0, 'data': []}
            else:
                data = {'message': 'Datos ya existen',
                        'error': 0, 'data': []}
        except Exception as e:
            data = {'message': 'Ha ocurrido un error interno. {}'.format(
                e.args), 'error': 2}
        return Response(data=data)


class EliminaEntrevistaPersona(APIView):
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def post(self, request, *args, **kwargs):
        data = {'message': 'Petición no procesada', 'error': 1}
        try:
            investigacion_id = self.kwargs['investigacion_id']
            ep = EntrevistaPersona.objects.filter(
                investigacion_id=investigacion_id).delete()

            data = {'message': 'Datos eliminados',
                    'error': 0, 'data': []}
        except Exception as e:
            data = {'message': 'Ha ocurrido un error interno. {}'.format(
                e.args), 'error': 2}
        return Response(data=data)


'''
 Formularios
'''


class EntrevistaPersonaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = EntrevistaPersona.objects.all()
    serializer_class = EntrevistaPersonaSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def get_queryset(self):
        investigacion_id = self.kwargs['investigacion_id']
        qs = self.queryset.filter(investigacion_id=investigacion_id)
        return qs


class EntrevistaAcademicaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaAcademica.objects.all()
    serializer_class = EntrevistaAcademicaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]
    


class EntrevistaActividadesHabitosViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaActividadesHabitos.objects.all()
    serializer_class = EntrevistaActividadesHabitosSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]
    


class EntrevistaAspectoCandidatoViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaAspectoCandidato.objects.all()
    serializer_class = EntrevistaAspectoCandidatoSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

class EntrevistaAspectoHogarViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaAspectoHogar.objects.all()
    serializer_class = EntrevistaAspectoHogarSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaAutomovilViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaAutomovil.objects.all()
    serializer_class = EntrevistaAutomovilSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaBienesRaicesViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaBienesRaices.objects.all()
    serializer_class = EntrevistaBienesRaicesSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

class EntrevistaCaracteristicasViviendaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaCaractaristicasVivienda.objects.all()
    serializer_class = EntrevistaCaracteristicasViviendaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

class EntrevistaCuentaDebitoViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaCuentaDebito.objects.all()
    serializer_class = EntrevistaCuentaDebitoSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaDeudaActualViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaDeudaActual.objects.all()
    serializer_class = EntrevistaDeudaActualSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaDireccionViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaDireccion.objects.all()
    serializer_class = EntrevistaDireccionSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaDistribucionDimensionesViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaDistribucionDimensiones.objects.all()
    serializer_class = EntrevistaDistribucionDimensionesSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaDocumentoCotejadoViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaDocumentoCotejado.objects.all()
    serializer_class = EntrevistaDocumentoCotejadoSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaEconomicaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaEconomica.objects.all()
    serializer_class = EntrevistaEconomicaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaGradoEscolaridadViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaGradoEscolaridad.objects.all()
    serializer_class = EntrevistaGradoEscolaridadSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaHistorialEnEmpresaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaHistorialEnEmpresa.objects.all()
    serializer_class = EntrevistaHistorialEnEmpresaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaInfoPersonalViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaInfoPersonal.objects.all()
    serializer_class = EntrevistaInfoPersonalSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaLicenciaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaLicencia.objects.all()
    serializer_class = EntrevistaLicenciaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaMiembroMarcoFamiliarViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaMiembroMarcoFamiliar.objects.all()
    serializer_class = EntrevistaMiembroMarcoFamiliarSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaOrigenViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaOrigen.objects.all()
    serializer_class = EntrevistaOrigenSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaOtroIdiomaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaOtroIdioma.objects.all()
    serializer_class = EntrevistaOtroIdiomaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaPropietarioViviendaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaPropietarioVivienda.objects.all()
    serializer_class = EntrevistaPropietarioViviendaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaReferenciaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaReferencia.objects.all()
    serializer_class = EntrevistaReferenciaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaSeguroViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaSeguro.objects.all()
    serializer_class = EntrevistaSeguroSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaSituacionViviendaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaSituacionVivienda.objects.all()
    serializer_class = EntrevistaSituacionViviendaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaSaludViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaSalud.objects.all()
    serializer_class = EntrevistaSaludSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaPrestacionViviendaViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaPrestacionVivienda.objects.all()
    serializer_class = EntrevistaPrestacionViviendaSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaTarjetaCreditoComercialViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaTarjetaCreditoComercial.objects.all()
    serializer_class = EntrevistaTarjetaCreditoComercialSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaTelefonoViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaTelefono.objects.all()
    serializer_class = EntrevistaTelefonoSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class EntrevistaTipoInmuebleViewSet(viewsets.ModelViewSet):
    queryset = EntrevistaTipoInmueble.objects.all()
    serializer_class = EntrevistaTipoInmuebleSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]


class DatosGeneralesFormApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,]

    def get_field_select(self, field):
        obj = field.get_internal_type()
        if obj == 'OneToOneField':
            print(' ==-> ', field.related_model.objects.all)
            # for data in field.related_model.objects.all():
            #    print(data)
        return ''

    def get_field_type(self, field):
        obj = field.get_internal_type()
        if obj == 'AutoField' or obj == 'IntegerField':
            return 'numeric'
        if obj == 'OneToOneField':
            self.get_field_select(field)
            return 'select'
        if obj == 'CharField':
            return 'text'
        if obj == 'TextField':
            return 'textarea'
        if obj == 'BooleanField':
            return 'boolean'
        if obj == 'ForeignKey':
            return 'numeric'
        return ''

    def get(self, request, *args, **kwargs):
        data = {'error': 1, 'message': 'Datos no procesados'}
        try:
            json_entrevista_academica = []
            json_entrevista_actividades_habitos = []
            json_entrevista_aspecto_candidato = []
            json_entrevista_aspecto_hogar = []
            json_entrevista_automovil = []
            json_entrevista_bienes_raices = []
            json_entrevista_cuenta_debito = []
            json_entrevista_deuda_actual = []
            json_entrevista_distribucion_dimensiones = []
            json_entrevista_documento_cotejado = []
            json_entrevista_economica = []
            json_entrevista_grado_escolaridad = []
            json_entrevista_historial_en_empresa = []
            json_entrevista_info_personal = []
            json_entrevista_miembro_marco_familiar = []
            json_origen = []
            json_entrevista_otro_idioma = []
            json_entrevista_persona = []
            json_licencia = []
            json_direccion = []
            json_entrevista_persona = []
            json_entrevista_propietario_vivienda = []
            json_entrevista_referencia = []
            json_entrevista_seguro = []
            json_entrevista_situacion_vivienda = []
            json_entrevista_salud = []
            json_entrevista_prestacion_vivienda = []
            json_entrevista_tarjeta_credito_comercial = []
            json_telefonos = []
            json_entrevista_tipo_inmueble = []

            for field in EntrevistaAcademica._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_academica.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaActividadesHabitos._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_actividades_habitos.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaAspectoCandidato._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_aspecto_candidato.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaAspectoHogar._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_aspecto_hogar.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaAutomovil._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_automovil.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaBienesRaices._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_bienes_raices.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaCuentaDebito._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_cuenta_debito.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaDeudaActual._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_deuda_actual.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaDireccion._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_direccion.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaDistribucionDimensiones._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_distribucion_dimensiones.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaDocumentoCotejado._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_documento_cotejado.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaEconomica._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_economica.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaEconomica._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_economica.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaGradoEscolaridad._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_grado_escolaridad.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaHistorialEnEmpresa._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_historial_en_empresa.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaInfoPersonal._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_info_personal.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaLicencia._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_licencia.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaMiembroMarcoFamiliar._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_miembro_marco_familiar.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaOrigen._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_origen.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaOtroIdioma._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_otro_idioma.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaPersona._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_persona.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaPropietarioVivienda._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_propietario_vivienda.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaReferencia._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_referencia.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaSeguro._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_seguro.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaSituacionVivienda._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_situacion_vivienda.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaSalud._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_salud.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaPrestacionVivienda._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_prestacion_vivienda.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaTarjetaCreditoComercial._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_tarjeta_credito_comercial.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaTelefono._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_telefonos.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            for field in EntrevistaTipoInmueble._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_entrevista_tipo_inmueble.append(
                        {'column_name': field.column, 'type': self.get_field_type(field), 'max_length': field.max_length})

            json_output = {
                'entrevista_academica': json_entrevista_academica,
                'entrevista_actividades_habitos': json_entrevista_actividades_habitos,
                'entrevista_aspecto_candidato': json_entrevista_aspecto_candidato,
                'entrevista_aspecto_hogar': json_entrevista_aspecto_hogar,
                'entrevista_automovil': json_entrevista_automovil,
                'entrevista_bienes_raices': json_entrevista_bienes_raices,
                'entrevista_cuenta_debito': json_entrevista_cuenta_debito,
                'entrevista_deuda_actual': json_entrevista_deuda_actual,
                'entrevista_direccion': json_direccion,
                'entrevista_distribucion_dimensiones': json_entrevista_distribucion_dimensiones,
                'entrevista_documento_cotejado': json_entrevista_documento_cotejado,
                'entrevista_economica': json_entrevista_economica,
                'entrevista_grado_escolaridad': json_entrevista_grado_escolaridad,
                'entrevista_historial_en_empresa': json_entrevista_historial_en_empresa,
                'entrevista_info_personal': json_entrevista_info_personal,
                'entrevista_licencia': json_licencia,
                'entrevista_miembro_marco_familiar': json_entrevista_miembro_marco_familiar,
                'entrevista_origen': json_origen,
                'entrevista_otro_idioma': json_entrevista_otro_idioma,
                'entrevista_persona': json_entrevista_persona,
                'entrevista_persona': json_entrevista_persona,
                'entrevista_propietario_vivienda': json_entrevista_propietario_vivienda,
                'entrevista_referencia': json_entrevista_referencia,
                'entrevista_seguro': json_entrevista_seguro,
                'entrevista_situacion_vivienda': json_entrevista_situacion_vivienda,
                'entrevista_salud': json_entrevista_salud,
                'entrevista_prestacion_vivienda': json_entrevista_prestacion_vivienda,
                'entrevista_tarjeta_credito_comercial': json_entrevista_tarjeta_credito_comercial,
                'entrevista_telefono': json_telefonos,
                'entrevista_tipo_inmueble': json_entrevista_tipo_inmueble
            }

            data = {'error': 0, 'message': 'Datos procesados correctamente',
                    'seccion': 'datos_generales', 'data': json_output}
        except Exception as e:
            data = {'error': 1,
                    'message': 'Datos no procesados. {}'.format(str(e))}
        return Response(data=data)
