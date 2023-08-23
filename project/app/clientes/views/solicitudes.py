# -*- coding: utf-8 -*-
import json
from datetime import date, datetime

from app.adjuntos.models import Adjuntos
from app.clientes.models import (ClienteSolicitud, ClienteSolicitudCandidato,
                                 ClienteUser)
from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Municipio, UserMessage
from app.investigacion.models import Investigacion, InvestigacionFactura, Psicometrico
from app.persona.models import Persona, Telefono
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from ..forms.cliente_solicitud_candidato_forms import \
    ClienteSolicitudCandidatoForm
from utils.general_utils import CreateGroupMessaje


class InitialClient(LoginRequiredMixin, TemplateView):

    template_name = 'clientes/initial_test.html'

    def get_context_data(self, **kwargs):
        context = super(InitialClient, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class ClienteSolicitudListView(LoginRequiredMixin, ListView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    model = ClienteSolicitud
    paginate_by = 25

    context_object_name = "cliente_solicitudes"
    template_name = 'clientes/solicitudes/solicitudes_list.html'

    def get_queryset(self):

        return ClienteSolicitud.objects.filter(cliente_id=self.request.user.id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudListView,
                        self).get_context_data(**kwargs)

        context['title'] = "Cliente / Listado de solicitudes"
        u = User.objects.get(id=self.request.user.pk)

        cliente_user = None
        try:
            cliente_user = ClienteUser.objects.get(username=u.username)
        except ClienteUser.DoesNotExist:
            print('Error en cliente_user')

        context['uc'] = cliente_user

        return context


class ClienteSolicitudCreateTemplateView(LoginRequiredMixin, TemplateView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):
        # cliente = Cliente.objects.get(user=request.user)
        u = User.objects.get(id=self.request.user.pk)
        cliente = ClienteUser.objects.get(username=u.username)
        solicitud = ClienteSolicitud()
        solicitud.cliente = cliente
        solicitud.save()
        return redirect('clientes:clientes_solicitud_detail', pk=solicitud.pk, **kwargs)


class ClienteSolicitudDetailView(LoginRequiredMixin, DetailView):

    # required
    group_required = [u"Client", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitud
    context_object_name = "cliente_solicitud"
    template_name = 'clientes/solicitudes/solicitud_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudDetailView,
                        self).get_context_data(**kwargs)

        context['title'] = "Cliente / Detalle de solicitud"
        csc = ClienteSolicitudCandidato.objects.filter(cliente_solicitud_id=self.object.pk)
        total_candidatos = csc.count()
        context['cliente_solicitud_candidatos'] = csc
        context['total_candidatos'] = total_candidatos
        context['solicitud_id'] = self.kwargs['pk']

        return context


class ClienteSolicitudEnviarTemplateView(LoginRequiredMixin, TemplateView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):

        solicitud = ClienteSolicitud.objects.get(
            pk=self.kwargs['solicitud_id'])
        candidatos_solicitud = ClienteSolicitudCandidato.objects.filter(
            cliente_solicitud_id=self.kwargs['solicitud_id'])
        today = date.today()

        now = datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        day_month_year = '{}-{}-{}'.format(year, month, day)
        hora = '{}:{}'.format(hour, minute)

        fecha_hora = '{} {}'.format(day_month_year, hora)

        # Tipo de investigaciones
        # Laboral,
        # Visita Domiciliaria (Enrevista),
        # Psicometrica
        # Validacion de Demanda,
        #
        # En Conjunto:
        # Socio económina= Laboral + Visita Domiciliaria
        # Visita Domiciliaria con demanda
        # Ojo: Todos tienen demanda

        # Asocuación de campos

        # Listado de candidato de la solicitud.
        # en Listado de candidatos tener estado por cada servico asociado
        '''
        De investiacacion

        agente  (Para el coordinador)
        solicitud = ClienteSolicitud
        candidato = Persona
        compania = Compania
        sucursal = Sucursales
        contacto = Contacto, on_delete=models.CASCADE
        fecha_recibido = DateField
        hora_recibido = CharField
        puesto = models.CharField(max_length=140)

        tipo_investigacion_status
        '''

        for candidato in candidatos_solicitud:

            candidato.fecha_envio = now
            candidato.save()

            # Buscar Candidato si no existe crearlo
            try:
                persona = Persona.objects.get(nss=candidato.nss, curp=candidato.curp)
                # persona.estado_id = candidato.estado_id
                # persona.municipio_id = candidato.municipio_id
                # Los datos de cada persona se debe validad por cada investigacion en este caso se coloca un flag para validad
                persona.datos_validados = False
                persona.puesto = candidato.puesto
                persona.save()
            except Persona.DoesNotExist:
                persona = Persona()
                persona.nss = candidato.nss
                persona.nombre = candidato.nombre
                persona.apellido = candidato.apellido
                persona.email = candidato.email
                persona.curp = candidato.curp
                persona.puesto = candidato.puesto
                # persona.estado_id = candidato.estado_id
                # persona.municipio_id = candidato.municipio_id

                persona.save()
                print('##### Persona creada #####')
                print('Persona creada', persona.pk)

            # agergar telefonos
            if candidato.telefono_casa:
                tel_casa = Telefono()
                tel_casa.persona = persona
                tel_casa.numero = candidato.telefono_casa
                tel_casa.categoria = 'casa'
                tel_casa.save()
            
            if candidato.telefono_movil:
                tel_casa = Telefono()
                tel_casa.persona = persona
                tel_casa.numero = candidato.telefono_movil
                tel_casa.categoria = 'movil'
                tel_casa.save()

            # Verifica tipo de serivico solicitados por el cliente
            entrevista_1 = False
            investigacion_laboral_2 = False
            psicometrico_3 = False

            for tInv in candidato.tipo_investigacion.all():
                if tInv.pk == 1:
                    investigacion_laboral_2 = True
                if tInv.pk == 3:
                    psicometrico_3 = True
                if tInv.pk == 2:
                    entrevista_1 = True
                    investigacion_laboral_2 = True
                if tInv.pk == 5:
                    entrevista_1 = True
                if tInv.pk == 4:
                    entrevista_1 = True

            print('Crear solicitud para candidato')

            investigacion = Investigacion()
            investigacion.cliente_solicitud_candidato = candidato
            investigacion.cliente_solicitud = solicitud
            investigacion.candidato = persona
            investigacion.compania = candidato.cliente_solicitud.cliente.compania
            investigacion.sucursal = candidato.sucursal
            investigacion.puesto = candidato.puesto

            # Programacion de la secuencia de la investigacion
            investigacion.entrevista = entrevista_1
            investigacion.laboral = investigacion_laboral_2
            investigacion.psicometrico = psicometrico_3

            # Colocar fecha y hora de envio por parte del cliente
            investigacion.fecha_recibido = today
            investigacion.hora_recibido = hora
            investigacion.save()

            adjuntos = Adjuntos(investigacion=investigacion).save()

            # Toma los valores de los tipo de solicitud

            for tInv in candidato.tipo_investigacion.all():
                investigacion.tipo_investigacion.add(tInv)

            # Crear el adjunto

            # Generación de elementos adicionales de la investigacion
            if entrevista_1:
                # Verificar si existe registros para la entrevista
                # No se puede generar en este momento por no tener el gestor..
                # Crearlo en el momento de la asignacion del gestor
                # ep = EntrevistaPersonaService(investigacion.id).verifyData()
                pass

            if psicometrico_3:
                psicometrico = Psicometrico()
                psicometrico.investigacion = investigacion
                psicometrico.save()

            print('##############################')
            print('Investigacion creada con el id: ' + str(investigacion.pk))

            # Enviar notificacion a cliente y coordinador de ejecutivos
            # Notificar a Coordinador de Ejecutivos

            # Notificar a los coordinadores de ejecutivos por email

            mail_data = {
                'mensaje': 'Se ha generado una nueva solicitud de investigación',
                'candidato': candidato.nombre + ' ' + candidato.apellido,
                'compania': solicitud.cliente.compania.nombre,
                'tipo_de_solicitud': investigacion.tipo_investigacion.all(),
                'fecha_solicitud': today,
                'url_detalles': 'http://127.0.0.1:8000/investigaciones/investigaciones/detail/' + str(solicitud.pk) + '/',
                'texto_url_detalles': 'Detalles de la solicitud',
                'email_coordinadores_de_ejecutivos': ['e@01.com', ],
            }
            # send_email('notificacion_coordinador_ejecutivo', mail_data)

            # Genera las facturas al cliente
            for csc in candidato.tipo_investigacion.all():
                factura = InvestigacionFactura()
                factura.investigacion_id = investigacion.pk
                factura.cantidad = 1
                factura.descripcion = csc
                factura.monto = csc.costo
                factura.save()

            # Notificar a los Coord. de Atención a Clientes y a Cobranzas
            CreateGroupMessaje().create_group_message("Cobranzas", investigacion.pk)
            CreateGroupMessaje().create_group_message("Coord. de Atención a Clientes", investigacion.pk)

        # cambiar la solicitud a enviada
        solicitud.enviado = True
        solicitud.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'El solicitud ha sido enviada satisfactoriamente.')
        return redirect('clientes:clientes_solicitud_detail', pk=solicitud.pk,)


class ClienteSolicitudDeleteView(LoginRequiredMixin, DeleteView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    model = ClienteSolicitud
    template_name = 'clientes/solicitudes/solicitud_confirm_delete.html'
    success_url = reverse_lazy('clientes:clientes_solicitudes_list')

    page = {
        'title': 'Eliminar Solicitud',
        'subtitle': 'delete file'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudDeleteView,
                        self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class ClienteSolicitudCandidatoCreateView(LoginRequiredMixin, CreateView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    # model = ClienteSolicitudCandidato
    form_class = ClienteSolicitudCandidatoForm  
    template_name = 'clientes/solicitudes/candidatos/candidato_form.html'
    # fields = ['nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'sucursal',
    #           'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud', 'telefono_casa', 'telefono_movil', 'direccion_fiscal']

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoCreateView,
                        self).get_context_data(**kwargs)
        
        context['title'] = "Cliente / Formulario de candidatos"

        solicitud = ClienteSolicitud.objects.get(pk=self.kwargs['solicitud_id'])
        context['form'].fields['sucursal'].queryset = Sucursales.objects.filter(compania_id=solicitud.cliente.compania_id)
        context['form'].fields['direccion_fiscal'].queryset = DireccionFiscal.objects.filter(compania_id=solicitud.cliente.compania_id)

        context['solicitud_id'] = self.kwargs['solicitud_id']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.cliente_solicitud_id = self.kwargs['solicitud_id']
        self.object.save()

        return super(ClienteSolicitudCandidatoCreateView, self).form_valid(form)

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El candidato ha sido creado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})


class ClienteSolicitudCandidatoUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    model = ClienteSolicitudCandidato
    template_name = 'clientes/solicitudes/candidatos/candidato_form.html'
    fields = ['nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'sucursal',
              'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud', 'telefono_casa', 'telefono_movil', 'direccion_fiscal']

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoUpdateView,
                        self).get_context_data(**kwargs)
        
        solicitud = ClienteSolicitud.objects.get(pk=self.kwargs['solicitud_id'])
        context['form'].fields['sucursal'].queryset = Sucursales.objects.filter(compania_id=solicitud.cliente.compania_id)
        context['form'].fields['direccion_fiscal'].queryset = DireccionFiscal.objects.filter(compania_id=solicitud.cliente.compania_id)

        context['solicitud_id'] = self.kwargs['solicitud_id']
        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El candidato ha sido actualizado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})


class ClienteSolicitudCandidatoDeleteView(LoginRequiredMixin, DeleteView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    model = ClienteSolicitudCandidato
    template_name = 'clientes/solicitudes/candidatos/candidato_confirm_delete.html'

    page = {
        'title': 'Eliminar candidato de Solicitud',
        'subtitle': 'delete file'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoDeleteView,
                        self).get_context_data(**kwargs)
        context['page'] = self.page
        context['solicitud'] = ClienteSolicitud.objects.get(
            pk=self.kwargs['solicitud_id'])

        return context

     # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El candidato ha sido eliminado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})


class MunicipiosView(View):

    def get(self, context, **response_kwargs):
        efe_key = self.kwargs['efe_key']
        # e = Estado.objects.get(efe_key=efe_key)
        municipios_list = Municipio.objects.filter(efe_key=efe_key).values(
            'id', 'municipio',).order_by('-municipio')
        # municipios_list = Municipio.objects.all().values('catalog_key', 'efe_key', 'municipio',).order_by('-municipio')
        response = [r for r in municipios_list]

        return HttpResponse(json.dumps(response))


class ClienteSolicitudObservacionUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = u"Cliente"
    raise_exception = True

    model = ClienteSolicitud
    template_name = 'clientes/solicitudes/solicitud_form.html'
    fields = ['observaciones']

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudObservacionUpdateView,
                        self).get_context_data(**kwargs)

        context['solicitud_id'] = self.kwargs['pk']
        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS,
            'La solicitud ha sido actualizada satisfactoriamente.')

        return reverse(
            'clientes:clientes_solicitud_detail',
            kwargs={"pk": self.kwargs['pk']}
        )
