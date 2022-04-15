from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from app.agente.models import GestorInfo
from app.api.serializer import InvestigacionSerializer, InvestigacionListSerializer, AdjuntosSerializer
from app.entrevista.models import EntrevistaTelefono, EntrevistaPersona, EntrevistaDireccion, EntrevistaOrigen, \
    EntrevistaLicencia
from app.investigacion.models import Investigacion
from app.adjuntos.models import Adjuntos
import uuid

from app.persona.models import DatosGenerales


class AsignacionInvestigacionApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = {'message': 'Petición no procesada', 'error': 1}
        try:
            gestor = GestorInfo.objects.get(usuario=self.request.user)
            queryset = Investigacion.objects.filter(gestorinvestigacion__gestor=gestor, gestorinvestigacion__estatus=2)
            serializer = InvestigacionListSerializer(queryset, many=True)
            data = {'message': 'Datos correctos', 'error': 0, 'data': serializer.data}
        except Exception as e:
            data = {'message': 'Ha ocurrido un error interno. {}'.format(e.args), 'error': 2}
        return Response(data=data)


class InvestigacionDetailApiView(ListAPIView):
    model = Investigacion
    serializer_class = InvestigacionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Investigacion.objects.filter(pk=self.kwargs.get('pk'))


class InvestigacionUploadImageApiView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_class = (FileUploadParser,)

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('inv'):
            queryset = Adjuntos.objects.filter(investigacion_id=self.request.GET.get('inv'))
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
                data={'error': 4, 'message': 'Archivo no encontrado, inténtelo nuevamente usando datos correctos.'},
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
                adjunto = Adjuntos.objects.filter(investigacion_id=investigacion_id)
                if not adjunto:
                    Adjuntos.objects.create(investigacion_id=investigacion_id)
                    adjunto = Adjuntos.objects.filter(investigacion_id=investigacion_id)
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


'''
 Formularios
'''


class DatosGeneralesFormApiView(APIView):
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
            json_data_ep = []
            json_telefonos = []
            json_direccion = []
            json_origen = []
            json_licencia = []

            for field in EntrevistaPersona._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_data_ep.append({'column_name': field.column, 'type': self.get_field_type(field)})


            for field in EntrevistaTelefono._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_telefonos.append({'column_name': field.column, 'type': self.get_field_type(field)})


            for field in EntrevistaDireccion._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_direccion.append({'column_name': field.column, 'type': self.get_field_type(field)})


            for field in EntrevistaOrigen._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_origen.append({'column_name': field.column, 'type': self.get_field_type(field)})


            for field in EntrevistaLicencia._meta.get_fields():
                if not field.one_to_many:
                    print(field.get_internal_type(), ' = ', field.column)
                    json_licencia.append({'column_name': field.column, 'type': self.get_field_type(field)})


            json_output= {'entrevista_persona':json_data_ep, 'entrevista_telefono':json_telefonos,'entrevista_origen': json_origen,'entrevista_licencia': json_licencia}

            data = {'error': 0, 'message': 'Datos procesados correctamente', 'seccion': 'datos_generales', 'data': json_output}
        except Exception as e:
            data = {'error': 1, 'message': 'Datos no procesados. {}'.format(str(e))}
        return Response(data=data)
