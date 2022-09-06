from multiprocessing import context
from re import L

from app.clientes.models import ClienteSolicitudCandidato, ClienteSolicitud, Cliente, ClienteTipoInvestigacion
from app.compania.forms import *
from app.compania.models import Compania
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.entrevista.models import EntrevistaPersona
from app.entrevista.services import *
from app.investigacion.forms import *
from app.persona.form_functions import *
from app.persona.forms import *
from app.persona.models import *
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from certifi import contents
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework import mixins, viewsets
from utils.general_utils import GetDataTime
from utils.send_mails import send_email

from .models import (GestorInvestigacion, Investigacion, InvestigacionBitacora,
                     Psicometrico)
from .serializers import InvestigacionSerializer
from app.persona.models import Demanda


class InvestigacionTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigaciones_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones /  Coordinador de atención al cliente'

        return context


class InvestigacionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):

        user = self.request.user
        companias_pk = Compania.objects.filter(
            coordinador_ejecutivos_id=user.pk).values_list('pk', flat=True)

        try:
            qs = self.queryset.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk).order_by("last_modified")
        except Compania.DoesNotExist:
            return self.queryset.none()

        # qs = self.queryset.filter(
        #          cliente_solicitud__isnull=False ).order_by("last_modified")

        return qs


class InvestigacionCandidatoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigaciones_candidatos_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCandidatoTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones'

        return context


class InvestigacionCandidatoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False, candidato_validado=False).order_by("cliente_solicitud")

        return qs


# Ejecutivo de visitas domiciliarias
class InvestigacionEjecutivoVisitaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/ejecutivo_visitas/investigaciones_ejecutivo_visitas_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoVisitaTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones / Ejecutivo de visitas domiciliarias'

        return context


class InvestigacionEjecutivoVisitaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False,
            candidato_validado=True,
            # agente__isnull=True,
            # coordinador_visitas_id=self.request.user.pk
        ).order_by("cliente_solicitud")

        return qs


class InvestigacionEjecutivoVisitaDetailView(DetailView):

    '''Detalle general para el Coorsinador de visitas'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/ejecutivo_visitas/investigaciones_ejecutivo_visita_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoVisitaDetailView,
                        self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['investigacion'] = inv

        context['title'] = 'Investigaciones / Coordinador de visitas domiciliarias / Detalles'

        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=inv, user_id=self.request.user.pk).order_by('-datetime')

        try:
            gInv = GestorInvestigacion.objects.get(
                investigacion=inv)
        except GestorInvestigacion.DoesNotExist:
            gInv = None

        context['gestor'] = gInv

        return context


class InvestigacionEjecutivoVisitaUpdateView(UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    fields = ['ejecutivo_visitas']
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/ejecutivo_visitas/investigaciones_ejecutivo_visita_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoVisitaUpdateView, self).get_context_data(**kwargs)

        context['form'].fields['ejecutivo_visitas'].queryset = User.objects.filter(groups__name='Ejecutivo de Visitas')

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = self.object
        bitacora.servicio = "Coordinador de visitas"
        bitacora.observaciones = "Actualizacion de asignación de gestor de visitas"
        bitacora.save()

        return super(InvestigacionEjecutivoVisitaUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El ejecutivo de visita ha sido actualizado')
        return reverse('investigaciones:investigaciones_coordinador_visitas_detail', kwargs={"pk": self.kwargs['pk']})


# --------------------------------------------------------------
# Cambiar coordinador de visita por ejecutivo
class InvestigacionCoordiandorVisitaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/coordinador_visitas/investigaciones_coordinador_visitas_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordiandorVisitaTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones / Coordinador de visitas domiciliarias'

        return context



class InvestigacionCoodinadorVisitaDetailView(DetailView):

    '''Detalle general para el Coorsinador de visitas'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/coordinador_visitas/investigacion_coordinador_visita_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoodinadorVisitaDetailView,
                        self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['title'] = 'Investigaciones / Coordinador de visitas domiciliarias / Detalles'

        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=inv, user_id=self.request.user.pk).order_by('-datetime')

        context['demandas'] = Demanda.objects.filter(persona=inv.candidato)

        return context


class InvestigacionCoordinadorVisitaCreateView(CreateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = GestorInvestigacion
    fields = ['gestor', 'fecha_asignacion']
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/coordinador_visitas/investigacion_coordinador_visita_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorVisitaCreateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        inv.agente_id = self.object.gestor.usuario.pk
        inv.save()

        ep = EntrevistaPersonaService(inv.id).verifyData()

        inv.entrevista_asignacion_visita_domiciliaria = True
        inv.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de visitas"
        bitacora.observaciones = "Asignación de gestor de visitas"
        bitacora.save()

        return super(InvestigacionCoordinadorVisitaCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El gestor ha sido asignado')
        return reverse('investigaciones:investigaciones_ejecutivo_visitas_detail', kwargs={"seccion_entrevista": "datos_generales", "pk": self.kwargs['investigacion_id']})


class InvestigacionCoordinadorVisitaUpdateView(UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = GestorInvestigacion
    fields = ['gestor', 'fecha_asignacion']
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/coordinador_visitas/investigacion_coordinador_visita_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorVisitaUpdateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        ep = EntrevistaPersonaService(inv.id).verifyData()

        inv.entrevista_asignacion_visita_domiciliaria = True
        inv.agente_id = self.object.gestor.usuario.pk
        inv.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de visitas"
        bitacora.observaciones = "Actualizacion de asignación de gestor de visitas"
        bitacora.save()

        return super(InvestigacionCoordinadorVisitaUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El gestor ha sido actualizado')
        return reverse('investigaciones:investigaciones_ejecutivo_visitas_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionCoodinadorVisitaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False,
            candidato_validado=True,
            # agente__isnull=True,
            # coordinador_visitas_id=self.request.user.pk
        ).order_by("cliente_solicitud")

        return qs


class InvestigacionEntrevistaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/edicion_enrtevista_personas/investigaciones_entrevistas_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEntrevistaTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones / Ejecutivo de visita domiciliaria'

        return context


class InvestigacionEntrevistaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False, candidato_validado=True, agente__isnull=False).order_by("cliente_solicitud")

        return qs


class InvestigacionDetailView(DetailView):

    '''Detalle general para el Coorsinador de Ejecutivos'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/investigacion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionDetailView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Investigaciones / Detalle de solicitud'

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['demandas'] = Demanda.objects.filter(persona=inv.candidato)

        try:
            entrevista_persona = EntrevistaPersona.objects.get(
                investigacion=inv)
        except EntrevistaPersona.DoesNotExist:
            entrevista_persona = None

        context['entrevista_persona'] = entrevista_persona

        return context


class InvestigacionEntrevistaDetailView(DetailView):

    '''Detalle general para el Coorsinador de Ejecutivos'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/entrevistas/investigaciones_entrevista_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEntrevistaDetailView, self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        persona = Persona.objects.get(pk=inv.candidato.pk)

        telefonos = Telefono.objects.filter(persona=persona)

        context['title'] = 'Investigaciones / Detalle de entrevista'

        context['telefonos'] = telefonos

        # context['bitacoras'] = InvestigacionBitacora.objects.filter(
        #     investigacion_id=self.kwargs['pk']).order_by('-datetime')

        # context['tajectorias_laborales'] = TrayectoriaLaboral.objects.filter(persona=inv.candidato).order_by('-fecha_creacion')

        # context['tajectorias_comerciales'] = TrayectoriaComercial.objects.filter(persona=inv.candidato)

        # try:
        #     gInv = GestorInvestigacion.objects.get(
        #         investigacion_id=self.kwargs['pk'])
        # except GestorInvestigacion.DoesNotExist:
        #     gInv = None

        # context['gestor'] = gInv

        # try:
        #     psicometrico = Psicometrico.objects.get(investigacion=inv)
        # except Psicometrico.DoesNotExist:
        #     psicometrico = None

        # context['psicometrico_data'] = psicometrico

        return context


class InvestigacionUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    # form_class = UserEditForm
    fields = ['agente', 'contacto', 'fecha_recibido', 'hora_recibido']
    success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/investigacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionUpdateView, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.resultado = 0
        self.object.status = 0
        self.object.status_general = 0
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'La investigación ha sido actualizada')

        super(InvestigacionUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class InvestigacionEjecutivoDeCuentaUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    fields = ['ejecutivo_de_cuentas', ]
    template_name = 'investigaciones/ejecutivo_de_cuenta/asignacion/asignacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoDeCuentaUpdateView,  self).get_context_data(**kwargs)

        context['title'] = 'Investigaciones - actualización de ejecutivo de cuenta'

        context['tipo_coordinador'] = "visitas"
        context['investigacion_id'] = self.kwargs['pk']
        context['form'].fields['ejecutivo_de_cuentas'].queryset = User.objects.filter(groups__name='Ejecutivo de cuentas')

        return context

    def form_valid(self, form):

        # inv = Investigacion.objects.get(id=self.kwargs['pk'])
        hoy = GetDataTime().get_current_date_time_in_format()

        self.object = form.save(commit=False)

        if self.object.coordinador_visitas:
            self.object.coord_visitas_asignado = True
            # Genera bitácora
            bitacora = InvestigacionBitacora()
            bitacora.user_id = self.request.user.pk
            bitacora.investigacion = self.object
            bitacora.servicio = "Coordinaron visitas"
            bitacora.observaciones = "Asignacion de ejecutivo de cuentas"
            bitacora.save()

            # Genera email
            mail_data = {
                'mensaje': 'Se ha asignado como coordinador de visitas',
                'candidato': self.object.candidato.nombre + ' ' + self.object.candidato.apellido,
                'compania': self.object.cliente_solicitud.cliente.compania.nombre,
                'tipo_de_solicitud': self.object.tipo_investigacion.all(),
                'fecha_solicitud': hoy,
                'url_detalles': 'http://127.0.0.1:8000/investigaciones/investigaciones/coordinador-visitas/detail/' + str(self.object.pk) + '/',
                'texto_url_detalles': 'Detalles de la solicitud',
                'email_coordinadores_de_visita': [self.object.coordinador_visitas.email, ],
            }
            # send_email('notificacion_coordinador_visita', mail_data)

            # Genera menaaje a usuario
            msj = UserMessage()
            msj.user = self.request.user

            msj.title = "Se ha asignado como ejecutivo de cuentas"
            msj.message = "Estimado usuario. Se ha generado una nueva solicitud, le invitamos a revisarla"
            msj.link = "/investigaciones/investigaciones/coordinador-visitas/detail/" +  str(self.object.pk)+"/"
            msj.save()
        else:
            self.object.coord_visitas_asignado = False

        self.object.save()

        return super(InvestigacionEjecutivoDeCuentaUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El coordiandor ha sido asignado')
        return reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['pk']})


class InvestigacionCoordVisitaUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    fields = ['coordinador_visitas', ]
    template_name = 'investigaciones/coordinador_ejectutivo_asignaciones/asignacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordVisitaUpdateView,  self).get_context_data(**kwargs)

        context['title'] = 'Investigaciones - actualización de coordinador de visita'

        context['tipo_coordinador'] = "visitas"
        context['investigacion_id'] = self.kwargs['pk']
        context['form'].fields['coordinador_visitas'].queryset = User.objects.filter(groups__name='Coordinador de visitas domiciliarias')

        return context

    def form_valid(self, form):

        # inv = Investigacion.objects.get(id=self.kwargs['pk'])
        hoy = GetDataTime().get_current_date_time_in_format()

        self.object = form.save(commit=False)

        if self.object.coordinador_visitas:
            self.object.coord_visitas_asignado = True
            # Genera bitácora
            bitacora = InvestigacionBitacora()
            bitacora.user_id = self.request.user.pk
            bitacora.investigacion = self.object
            bitacora.servicio = "Coordinador de ejecutivos"
            bitacora.observaciones = "Asignacion de coordinador de visitas"
            bitacora.save()

            # Genera email
            mail_data = {
                'mensaje': 'Se ha asignado como coordinador de visitas',
                'candidato': self.object.candidato.nombre + ' ' + self.object.candidato.apellido,
                'compania': self.object.cliente_solicitud.cliente.compania.nombre,
                'tipo_de_solicitud': self.object.tipo_investigacion.all(),
                'fecha_solicitud': hoy,
                'url_detalles': 'http://127.0.0.1:8000/investigaciones/investigaciones/coordinador-visitas/detail/' + str(self.object.pk) + '/',
                'texto_url_detalles': 'Detalles de la solicitud',
                'email_coordinadores_de_visita': [self.object.coordinador_visitas.email, ],
            }
            # send_email('notificacion_coordinador_visita', mail_data)

            # Genera menaaje a usuario
            msj = UserMessage()
            msj.user = self.request.user

            msj.title = "Se ha asignado como coordinador de visita"
            msj.message = "Estimado usuario. Se ha generado una nueva solicitud, le invitamos a revisarla"
            msj.link = "/investigaciones/investigaciones/coordinador-visitas/detail/" + \
                str(self.object.pk)+"/"
            msj.save()
        else:
            self.object.coord_visitas_asignado = False

        self.object.save()

        return super(InvestigacionCoordVisitaUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El coordiandor ha sido asignado')
        return reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['pk']})


class InvestigacionCoordPsicometricoUpdateView(UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    fields = ['coordinador_psicometrico', ]
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/coordinador_ejectutivo_asignaciones/asignacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordPsicometricoUpdateView, self).get_context_data(**kwargs)

        context['title'] = 'Investigaciones - actualización de coordinador de psicometrico'

        context['tipo_coordinador'] = "psicométrico"
        context['investigacion_id'] = self.kwargs['pk']
        context['form'].fields['coordinador_psicometrico'].queryset = User.objects.filter(groups__name='Coordinador Psicometrico')

        return context

    def form_valid(self, form):

        # inv = Investigacion.objects.get(id=self.kwargs['pk'])
        hoy = GetDataTime().get_current_date_time_in_format()

        self.object = form.save(commit=False)

        if self.object.coordinador_psicometrico:
            self.object.coord_psicometrico_asignadado = True
            # Genera bitácora
            bitacora = InvestigacionBitacora()
            bitacora.user_id = self.request.user.pk
            bitacora.investigacion = self.object
            bitacora.servicio = "Coordinador de ejecutivos"
            bitacora.observaciones = "Asignacion de coordinador de psicométrico"
            bitacora.save()

            # Genera email
            mail_data = {
                'mensaje': 'Se ha asignado como coordinador de visitas',
                'candidato': self.object.candidato.nombre + ' ' + self.object.candidato.apellido,
                'compania': self.object.cliente_solicitud.cliente.compania.nombre,
                'tipo_de_solicitud': self.object.tipo_investigacion.all(),
                'fecha_solicitud': hoy,
                'url_detalles': 'http://127.0.0.1:8000/investigaciones/investigaciones/coordinador-psicometrico/detail/' + str(self.object.pk) + '/',
                'texto_url_detalles': 'Detalles de la solicitud',
                'email_coordinadores_de_visita': [self.object.coordinador_psicometrico.email, ],
            }
            # send_email('notificacion_coordinador_visita', mail_data)

            # Genera menaaje a usuario
            msj = UserMessage()
            msj.user = self.request.user

            msj.title = "Asignacion de coordinador de psicométrico"
            msj.message = "Estimado usuario. Se ha generado una nueva solicitud, le invitamos a revisarla"
            msj.link = "/investigaciones/investigaciones/coordinador-psicometrico/detail/" + \
                str(self.object.pk)+"/"
            msj.save()
        else:
            self.object.coord_psicometrico_asignadado = False

        self.object.save()

        return super(InvestigacionCoordPsicometricoUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El coordiandor ha sido asignado')
        return reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['pk']})


class CandidatoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigacion_candidato_edit.html'

    def post(self, request, *args, **kwargs):

        investigacion = Investigacion.objects.select_related('compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        # agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        formCandidato = CandidatoAltaForm(request.POST, prefix='candidato', instance=investigacion.candidato)

        if formCandidato.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 'El candidato ha sido guardado')
            formCandidato.save()
            investigacion.candidato_validado = formCandidato.cleaned_data['datos_validados']
            if investigacion.candidato_validado:
                try:
                    csc = ClienteSolicitudCandidato.objects.get(pk=investigacion.cliente_solicitud_candidato_id)
                    if not csc.fecha_inicio:
                        csc.fecha_inicio = datetime.datetime.now()
                        csc.save()
                except:
                    pass
            investigacion.save()
            InvestigacionBitacora(investigacion_id=investigacion.id, user_id=request.user.pk,servicio='Candidato', observaciones='Candidato actualizado').save()
        else:
            msg_param = ''
        ####################### Origen #######################
        formOrigen = OrigenAltaForma(request.POST, prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(
            request.POST, prefix='origen')
        if has_info(request.POST, prefix='origen', investigacion=investigacion):
            if formOrigen.is_valid():
                origen = formOrigen.save(commit=False)
                origen.persona = investigacion.candidato
                origen.save()
            else:
                msg_param = ''
        ####################### Dirección #######################
        formDireccion = DireccionForm(request.POST, prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(
            request.POST, prefix='direccion')
        if has_info(request.POST, prefix='direccion', investigacion=investigacion):
            if formDireccion.is_valid():
                direccion = formDireccion.save(commit=False)
                direccion.persona = investigacion.candidato
                direccion.save()
            else:
                msg_param = ''
        ####################### Teléfono1 (casa)  #######################
        formTelefono1 = TelefonoForm(request.POST, prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(
            request.POST, prefix='telefono1')
        if has_info(request.POST, prefix='telefono1', investigacion=investigacion):
            if formTelefono1.is_valid():
                tel1 = formTelefono1.save(commit=False)
                tel1.persona = investigacion.candidato
                tel1.categoria = 'casa'
                tel1.save()
            else:
                msg_param = ''
        ####################### Teléfono2 (movil)  #######################
        formTelefono2 = TelefonoForm(request.POST, prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(
            request.POST, prefix='telefono2')
        if has_info(request.POST, prefix='telefono2', investigacion=investigacion):
            if formTelefono2.is_valid():
                tel2 = formTelefono2.save(commit=False)
                tel2.persona = investigacion.candidato
                tel2.categoria = 'movil'
                tel2.save()
            else:
                msg_param = ''
        ####################### Teléfono3 (recado)  #######################
        formTelefono3 = TelefonoForm(request.POST, prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(
            request.POST, prefix='telefono3')
        if has_info(request.POST, prefix='telefono3', investigacion=investigacion):
            if formTelefono3.is_valid():
                tel3 = formTelefono3.save(commit=False)
                tel3.persona = investigacion.candidato
                tel3.categoria = 'recado'
                tel3.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Infonavit #######################
        formPrestacionViviendaInfonavit = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit')
        if has_info(request.POST, prefix='prestacion_vivienda_infonavit', investigacion=investigacion):
            if formPrestacionViviendaInfonavit.is_valid():
                prestacionViviendaInfonavit = formPrestacionViviendaInfonavit.save(
                    commit=False)
                prestacionViviendaInfonavit.persona = investigacion.candidato
                prestacionViviendaInfonavit.categoria_viv = 'infonavit'
                prestacionViviendaInfonavit.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Fonacot #######################
        formPrestacionViviendaFonacot = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot')
        if has_info(request.POST, prefix='prestacion_vivienda_fonacot', investigacion=investigacion):
            if formPrestacionViviendaFonacot.is_valid():
                prestacionViviendaFonacot = formPrestacionViviendaFonacot.save(
                    commit=False)
                prestacionViviendaFonacot.persona = investigacion.candidato
                prestacionViviendaFonacot.categoria_viv = 'fonacot'
                prestacionViviendaFonacot.save()
            else:
                msg_param = ''
        ####################### Legalidad #######################
        formLegalidad = LegalidadAltaForma(
            request.POST, prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(request.POST, prefix='legalidad')
        if has_info(request.POST, prefix='legalidad', investigacion=investigacion):
            if formLegalidad.is_valid():
                legalidad = formLegalidad.save(commit=False)
                legalidad.persona = investigacion.candidato
                legalidad.save()
            else:
                msg_param = ''

        return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id']}))


    def get_context_data(self, **kwargs):
        context = super(CandidatoTemplateView, self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.select_related('compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        # agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        DemandaFormSet = modelformset_factory(
            Demanda, form=DemandaAltaForma, max_num=1, extra=1)

        context['title'] = "Investigaciones / Actualizacion datos del candidato"

        context['investigacion'] = investigacion

        context['formCandidato'] = CandidatoAltaForm(
            prefix='candidato', instance=investigacion.candidato)
        # context['formInvestigacion'] = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={
        #                                                        'compania': investigacion.compania.id}, agt_id=agente_id)
        context['formInvestigacion'] = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={'compania': investigacion.compania.id})
        context['formOrigen'] = OrigenAltaForma(prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(prefix='origen')
        context['formDireccion'] = DireccionForm(prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(prefix='direccion')
        context['formTelefono1'] = TelefonoForm( prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(prefix='telefono1')
        context['formTelefono2'] = TelefonoForm(prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(prefix='telefono2')
        context['formTelefono3'] = TelefonoForm(prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(prefix='telefono3')
        context['formPrestacionViviendaInfonavit'] = PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit')
        context['formPrestacionViviendaFonacot'] = PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot')
        context['formLegalidad'] = LegalidadAltaForma(prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(prefix='legalidad')
        context['formDemanda'] = DemandaFormSet(queryset=Demanda.objects.filter(persona=investigacion.candidato))
        context['formSeguro'] = SeguroAltaForma(prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(prefix='seguro')
        context['formSucursal'] = CompaniaSucursalForm(investigacion.compania.id, investigacion.sucursal.id if investigacion.sucursal else None, prefix='investigacion')

        return context


class ClienteSolicitudCreateTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Client", ]
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


class ClienteSolicitudDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = [u"Client", u"Coord. de Atención a Clientes"]
    raise_exception = True

    model = ClienteSolicitud
    context_object_name = "cliente_solicitud"
    template_name = 'clientes/solicitudes/solicitud_detail.html'

    page = {
        'title': 'Detalle de Solicitud',
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudDetailView,
                        self).get_context_data(**kwargs)

        context['page'] = self.page
        context['cliente_solicitud_candidatos'] = ClienteSolicitudCandidato.objects.filter(
            cliente_solicitud_id=self.object.pk)

        return context


class PersonaTrayectoriaCrearTemplateView(LoginRequiredMixin, TemplateView):

    # required
    group_required = [u"Client", ]
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):

        # Tomar investigacion
        investigacion = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])

        nva_trayectoria = TrayectoriaLaboral()
        nva_trayectoria.persona = investigacion.candidato
        nva_trayectoria.compania = investigacion.compania
        nva_trayectoria.save()

        Evaluacion(trayectoriaLaboral=nva_trayectoria).save()

        messages.add_message(self.request, messages.SUCCESS,
                             'El solicitud ha sido enviada satisfactoriamente.')
        return redirect(reverse('investigaciones:investigacion_persona_trayectoria_laboral_edit',
                                kwargs={"investigacion_id": self.kwargs['investigacion_id'], "pk": nva_trayectoria.pk, }))


class PersonaTrayectoriaEditTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/personas/trayectoria_laboral_form.html'

    # def post(self, request, *args, **kwargs):

    #     investigacion = Investigacion.objects.select_related(
    #         'compania', 'candidato').get(id=self.kwargs['investigacion_id'])

    #     return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))

    def post(self, request, *args, **kwargs):

        exito = True

        investigacion = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])
        trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(
            pk=self.kwargs['pk'])
        evaluacion = trayectoria_empresa.evaluacion_set.all()
        opinion_jefe = trayectoria_empresa.opinion_set.filter(
            categoria=1) if evaluacion else None
        opinion_rh = trayectoria_empresa.opinion_set.filter(
            categoria=2) if evaluacion else None

        carta_laboral = trayectoria_empresa.cartalaboral if hasattr(
            trayectoria_empresa, 'cartalaboral') else None
        datos_generales = trayectoria_empresa.datosgenerales if hasattr(
            trayectoria_empresa, 'datosgenerales') else None

        informantes = evaluacion[0].informante_set.all(
        ) if evaluacion else None

        informante1 = informantes[0] if informantes else None

        informante2 = (informantes[1] if informantes.count(
        ) > 1 else None) if informantes else None

        formTrayectoria = TrayectoriaForm(
            request.POST, prefix='trayectoria', instance=trayectoria_empresa)

        if formTrayectoria.is_valid():
            trayectoria_empresa = formTrayectoria.save()
        else:
            # logger.info('formTrayectoria invalid')
            print("####### 01 #######")
            print(formTrayectoria.errors.as_data())
            exito = False

        # Carta Laboral
        formCartaLaboral = CartaLaboralForma(
            request.POST, instance=carta_laboral)
        if formCartaLaboral.is_valid():
            carta_laboral = formCartaLaboral.save(commit=False)
            carta_laboral.trayectoriaLaboral = trayectoria_empresa
            carta_laboral.save()
        else:
            # logger.info('formCartaLaboral invalid')
            print("####### 02 #######")
            exito = False

        # Datos Generales
        formDatosGenerales = DatosGeneralesForma(
            request.POST, instance=datos_generales)
        if formDatosGenerales.is_valid():
            datos_generales = formDatosGenerales.save(commit=False)
            datos_generales.trayectoriaLaboral = trayectoria_empresa
            datos_generales.save()
        else:
            # logger.info('formDatosGenerales invalid')
            print("####### 03 #######")
            exito = False

        ############## Evaluación ##############
        formEvaluacion = EvaluacionForm(request.POST, prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(
            request.POST, prefix='evaluacion')

        if has_info_trayectoria(request.POST, prefix='evaluacion', trayectoria=trayectoria_empresa):
            if formEvaluacion.is_valid():
                evaluacion = formEvaluacion.save(commit=False)
                evaluacion.trayectoriaLaboral = trayectoria_empresa
                evaluacion.save()
            else:
                print("####### 05 #######")
                # logger.info('formEvaluacion invalid')
                exito = False

        ############## Opinion (Jefe) ##############
        formOpinionJefe = OpinionAltaForma(request.POST, prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(
            request.POST, prefix='opinion_jefe')

        if has_info_trayectoria(request.POST, prefix='opinion_jefe', trayectoria=trayectoria_empresa):
            if formOpinionJefe.is_valid():
                opinion_jefe = formOpinionJefe.save(commit=False)
                opinion_jefe.trayectoriaLaboral = trayectoria_empresa
                opinion_jefe.categoria = 1
                opinion_jefe.save()
            else:
                print("####### 05 #######")
                # logger.info('opinion_jefe invalid')
                exito = False

        ############## Opinion (RH) ##############
        formOpinionRH = OpinionAltaForma(request.POST, prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(
            request.POST, prefix='opinion_rh')
        if has_info_trayectoria(request.POST, prefix='opinion_rh', trayectoria=trayectoria_empresa):
            if formOpinionRH.is_valid():
                opinion_rh = formOpinionRH.save(commit=False)
                opinion_rh.trayectoriaLaboral = trayectoria_empresa
                opinion_rh.categoria = 2
                try:
                    opinion_rh.save()
                except Exception as error:
                    # logger.info('opinion_rh error')
                    # msg.append({
                    #     "text": "Opinion RH: " + str(error),
                    #     "status": "danger"
                    # })
                    print("####### 06 #######")
                    exito = False
            else:
                pass
                # logger.info('formOpinionRH invalid')
                exito = False

        ############## Informantes  ##############
        formInformante1 = InformanteAltaForma(
            request.POST, prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(request.POST, prefix='informante1')
        if has_info_trayectoria(request.POST, prefix='informante1', trayectoria=trayectoria_empresa):
            informante1 = formInformante1.save(commit=False)
            informante1.evaluacion = evaluacion
            informante1.save()

        formInformante2 = InformanteAltaForma(
            request.POST, prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(request.POST, prefix='informante2')
        if has_info_trayectoria(request.POST, prefix='informante2', trayectoria=trayectoria_empresa):
            informante2 = formInformante2.save(commit=False)
            informante2.evaluacion = evaluacion
            informante2.save()

        if exito:
            return redirect(reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))
            
    def get_context_data(self, **kwargs):
        context = super(PersonaTrayectoriaEditTemplateView,
                        self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])

        trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(
            pk=self.kwargs['pk'])
        evaluacion = trayectoria_empresa.evaluacion_set.all()
        opinion_jefe = trayectoria_empresa.opinion_set.filter(
            categoria=1) if evaluacion else None
        opinion_rh = trayectoria_empresa.opinion_set.filter(
            categoria=2) if evaluacion else None
        carta_laboral = trayectoria_empresa.cartalaboral if hasattr(
            trayectoria_empresa, 'cartalaboral') else None
        datos_generales = trayectoria_empresa.datosgenerales if hasattr(
            trayectoria_empresa, 'datosgenerales') else None

        informantes = evaluacion[0].informante_set.all(
        ) if evaluacion else None
        informante1 = informantes[0] if informantes else None
        informante2 = (informantes[1] if informantes.count(
        ) > 1 else None) if informantes else None

        datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

        formSucursal = CompaniaSucursalForm(
            trayectoria_empresa.compania.id, trayectoria_empresa.sucursal.id if trayectoria_empresa.sucursal else None, prefix='trayectoria')

        formTrayectoria = TrayectoriaForm(
            prefix='trayectoria', instance=trayectoria_empresa)

        formCartaLaboral = CartaLaboralForma(
            instance=carta_laboral) if carta_laboral else CartaLaboralForma()

        formDatosGenerales = DatosGeneralesForma(
            instance=datos_generales) if datos_generales else DatosGeneralesForma()

        formEvaluacion = EvaluacionForm(
            prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')

        formEvaluacion = EvaluacionForm(
            prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')

        formOpinionJefe = OpinionAltaForma(
            prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(prefix='opinion_jefe')

        formOpinionRH = OpinionAltaForma(
            prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(prefix='opinion_rh')

        formInformante1 = InformanteAltaForma(
            prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(prefix='informante1')

        formInformante2 = InformanteAltaForma(
            prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(prefix='informante2')

        context['investigacion'] = investigacion
        context['trayectoria_empresa'] = trayectoria_empresa
        context['evaluacion'] = evaluacion[0] if evaluacion else None
        context['opinion_jefe'] = opinion_jefe[0] if opinion_jefe else None
        context['opinion_rh'] = opinion_rh[0] if opinion_rh else None
        context['carta_laboral'] = carta_laboral
        context['datos_generales'] = datos_generales
        context['informante1'] = informante1
        context['informante2'] = informante2
        context['datos_entrevista'] = datos_entrevista
        context['formSucursal'] = formSucursal
        context['formTrayectoria'] = formTrayectoria
        context['formCartaLaboral'] = formCartaLaboral
        context['formDatosGenerales'] = formDatosGenerales
        context['formEvaluacion'] = formEvaluacion
        context['formOpinionJefe'] = formOpinionJefe
        context['formOpinionRH'] = formOpinionRH
        context['formInformante1'] = formInformante1
        context['formInformante2'] = formInformante2

        return context


class PersonaTrajectoriaComercialCrearTemplateView(LoginRequiredMixin, TemplateView):

    # required
    group_required = [u"Client", ]
    raise_exception = True

    template_name = 'investigaciones/personas/trayectoria_comercial_form.html'

    def post(self, request, *args, **kwargs):

        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        trayectoria_instance = TrayectoriaComercial.objects.get(id=self.kwargs['trayectoria_id']) if self.kwargs['trayectoria_id'] else None

        referencia_extra = 3 - TrayectoriaComercialReferencia.objects.filter(trayectoria_comercial=self.kwargs['trayectoria_id']).count() if self.kwargs['trayectoria_id'] else 3
        referencia_formset = modelformset_factory(TrayectoriaComercialReferencia, form=TrayectoriaComercialReferenciaForm, extra=referencia_extra)

        trayectoria_comercial_form = TrayectoriaComercialForm(request.POST, instance=trayectoria_instance)
        trayectoria_comercial_referencia_formset = referencia_formset(request.POST)

        if trayectoria_comercial_form.is_valid():
            trayectoria_comercial = trayectoria_comercial_form.save(
                commit=False)
            trayectoria_comercial.persona = investigacion.candidato
            trayectoria_comercial.save()

            if trayectoria_comercial_referencia_formset.is_valid():
                trayectoria_comercial_referencia = trayectoria_comercial_referencia_formset.save(
                    commit=False)
                for referencia in trayectoria_comercial_referencia:
                    referencia.trayectoria_comercial = trayectoria_comercial
                    referencia.save()

                bitacora = InvestigacionBitacora()
                bitacora.user_id = self.request.user.pk
                bitacora.investigacion = investigacion
                bitacora.servicio = "Coord. Ejecutivo"
                bitacora.observaciones = "Creación de trayectoria comercial"
                bitacora.save()

                return redirect(reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))

    def get_context_data(self, **kwargs):

        context = super(PersonaTrajectoriaComercialCrearTemplateView,
                        self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])
        trayectoria_instance = TrayectoriaComercial.objects.get(
            id=self.kwargs['trayectoria_id']) if self.kwargs['trayectoria_id'] else None

        referencia_extra = 3 - TrayectoriaComercialReferencia.objects.filter(
            trayectoria_comercial_id=self.kwargs['trayectoria_id']).count() if self.kwargs['trayectoria_id'] else 3
        referencia_formset = modelformset_factory(
            TrayectoriaComercialReferencia, form=TrayectoriaComercialReferenciaForm, extra=referencia_extra)

        trayectoria_comercial_form = TrayectoriaComercialForm(
            instance=trayectoria_instance)

        # referencial_queryset = TrayectoriaComercialReferencia.objects.none()
        referencial_queryset = TrayectoriaComercialReferencia.objects.filter(
            trayectoria_comercial=self.kwargs['trayectoria_id']) if self.kwargs['trayectoria_id'] else TrayectoriaComercialReferencia.objects.none()
        trayectoria_comercial_referencia_formset = referencia_formset(
            queryset=referencial_queryset)

        context['investigacion'] = investigacion
        context['trayectoria_comercial_form'] = trayectoria_comercial_form
        context['trayectoria_comercial_referencia_formset'] = trayectoria_comercial_referencia_formset

        return context


class PersonaTrajectoriaComercialDeleteTemplateView(LoginRequiredMixin, TemplateView):

    # required
    group_required = [u"Client", ]
    raise_exception = True

    def get(self, request, *args, **kwargs):

        investigacion = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])

        trayectoria_id = str(self.kwargs['trayectoria_id'])
        investigacion_id = str(self.kwargs['investigacion_id'])

        trayectoria_comercial_referencia = TrayectoriaComercialReferencia.objects.get(
            id=self.kwargs['pk'])
        trayectoria_comercial_referencia.delete()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = investigacion
        bitacora.servicio = "Coord. Ejecutivo"
        bitacora.observaciones = "Eliminacion de referencia de trayectoria comercial"
        bitacora.save()

        return HttpResponseRedirect('/investigaciones/investigaciones/persona/trayectoria-comercial/create/'+investigacion_id+'/'+trayectoria_id+'/')


class InvestigacionCoordinadorPsicometricoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False,
            candidato_validado=True,
            psicometrico=True,
            coordinador_psicometrico_id=self.request.user.pk
        ).order_by("cliente_solicitud")

        return qs


class InvestigacionCoordinadorPsicometricoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/coordinador_psicometrico/investigaciones_coordinador_psicometrico_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorPsicometricoTemplateView,
                        self).get_context_data(**kwargs)

        context['title'] = "Investigaciones / Coordinador psicométrico"

        return context


class InvestigacionCoordinadorPsicometricoDetailView(LoginRequiredMixin, DetailView):

    '''Detalle general para el Coorsinador de visitas'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/coordinador_psicometrico/investigaciones_coordinador_psicometrico_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorPsicometricoDetailView,
                        self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=inv, user_id=self.request.user.pk).order_by('-datetime')

        try:
            psicometrico = Psicometrico.objects.get(investigacion=inv)
        except Psicometrico.DoesNotExist:
            psicometrico = None

        context['psicometrico_data'] = psicometrico
        context['investigacion_id'] = inv.id

        return context


class InvestigacionCoordinadorPsicometricoCreateView(LoginRequiredMixin, CreateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Psicometrico
    fields = ['user', ]
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/coordinador_psicometrico/investigaciones_coordinador_psicometrico_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorPsicometricoCreateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        inv.psicometrico_ejecutivo_asignado = True
        inv.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de Psicometrico"
        bitacora.observaciones = "Asignación de ejecutivo"
        bitacora.save()

        return super(InvestigacionCoordinadorPsicometricoCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El ejecutivo ha sido asignado')
        return reverse('investigaciones:investigaciones_coordinador_psicometrico_detail', kwargs={"investigacion_id": self.kwargs['investigacion_id']})


class InvestigacionCoordinadorPsicometricoUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = [u"Administrator", ]
    raise_exception = True

    model = Psicometrico
    fields = ['user', ]
    template_name = 'investigaciones/coordinador_psicometrico/investigaciones_coordinador_psicometrico_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorPsicometricoUpdateView,
                        self).get_context_data(**kwargs)
        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.save()

        inv.psicometrico_ejecutivo_asignado = True
        inv.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de psicometrico"
        bitacora.observaciones = "Actualizacion de asignación de gestor de psicometrico"
        bitacora.save()

        return super(InvestigacionCoordinadorPsicometricoUpdateView, self).form_valid(form)

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Ejecutivo ha sido actualizado')
        return reverse('investigaciones:investigaciones_coordinador_psicometrico_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionEjecutivoPsicometricoList(LoginRequiredMixin, ListView):

    # required
    group_required = [u"Creator", ]
    raise_exception = True

    model = Psicometrico
    paginate_by = 25

    context_object_name = "psicometricos"
    template_name = 'investigaciones/ejecutivo_psicometrico/ejecutivo_psicometrico_list.html'

    # TODO: add a filter for the user
    def get_queryset(self):
        # return Psicometrico.objects.filter(user_id=self.request.user.id).order_by('-created')
        return Psicometrico.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoPsicometricoList,
                        self).get_context_data(**kwargs)

        context['title'] = "Inveatigaciones / Ejecutivo de psicométrico"

        return context


class InvestigacionEjecutivoPsicometricoUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Psicometrico
    fields = ['observaciones', 'archivo', 'completado']
    template_name = 'investigaciones/ejecutivo_psicometrico/ejecutivo_psicometrico_form.html'

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.save()

        if self.object.completado and self.object.archivo:
            inv.psicometrico_completado = True
            inv.save()
        else:
            inv.psicometrico_completado = False
            inv.save()
            self.object.completado = False

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Ejecutivo de psicometrico"
        bitacora.observaciones = "Actualizacion de asignación de gestor de psicometrico"
        bitacora.save()

        return super(InvestigacionEjecutivoPsicometricoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoPsicometricoUpdateView,
                        self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(
            pk=self.kwargs['investigacion_id'])

        context['title'] = "Inveatigaciones / Ejecutivo de psicométrico / Formulario"

        context['investigacion'] = investigacion

        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El ejecutivo ha sido asignado')
        return reverse('investigaciones:investigaciones_ejecutivo_psicometrico_list')


class InvestigacionEjecutivoPsicometricoDetailView(LoginRequiredMixin, DetailView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Psicometrico
    context_object_name = "psicometrico_data"
    template_name = 'investigaciones/ejecutivo_psicometrico/ejecutivo_psicometrico_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoPsicometricoDetailView,
                        self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(
            pk=self.kwargs['investigacion_id'])
        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=investigacion, user_id=self.request.user.pk).order_by('-datetime')

        context['investigacion'] = investigacion

        return context

# se cambia el nombre de ejecutivo laboral por ejecutivo de cuenta en la interfaz
class InvestigacionEjecutivoLaboralTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/ejecutivo_de_cuenta/investigaciones_ejecutivo_lab_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoLaboralTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones / Ejecutivo de cuentas'

        return context


class InvestigacionEjecutivoLaboralViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):

        qs = self.queryset.filter(
                 cliente_solicitud__isnull=False, ejecutivo_de_cuentas=self.request.user).order_by("last_modified")

        return qs


class InvestigacionEjecutivoLaboralDetailView(DetailView):

    '''Detalle general para el Coorsinador de Ejecutivos'''

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/ejecutivo_de_cuenta/investigaciones_ejecutivo_lab_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoLaboralDetailView, self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['title'] = "Inveatigaciones / Ejecutivo de cuenta / Detalle de solicitud "

        context['bitacoras'] = InvestigacionBitacora.objects.filter(investigacion_id=self.kwargs['pk'], user=self.request.user).order_by('-datetime')

        context['tajectorias_laborales'] = TrayectoriaLaboral.objects.filter(persona=inv.candidato)

        context['tajectorias_comerciales'] = TrayectoriaComercial.objects.filter(persona=inv.candidato)

        context['demandas'] = Demanda.objects.filter(persona=inv.candidato)

        return context


class InvestigacionEjecutivoLaboralCandidatoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigacion_edv_candidato_edit.html'

    def post(self, request, *args, **kwargs):

        investigacion = Investigacion.objects.select_related(
            'compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        # agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        formCandidato = CandidatoAltaForm(
            request.POST, prefix='candidato', instance=investigacion.candidato)

        if formCandidato.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 'El candidato ha sido guardado')
            formCandidato.save()
            investigacion.candidato_validado = formCandidato.cleaned_data['datos_validados']
            if investigacion.candidato_validado:
                try:
                    csc = ClienteSolicitudCandidato.objects.get(
                        pk=investigacion.cliente_solicitud_candidato_id)
                    if not csc.fecha_inicio:
                        csc.fecha_inicio = datetime.datetime.now()
                        csc.save()
                except:
                    pass
            investigacion.save()
            InvestigacionBitacora(investigacion_id=investigacion.id, user_id=request.user.pk,
                                  servicio='Candidato', observaciones='Candidato actualizado').save()
        else:
            msg_param = ''
        ####################### Origen #######################
        formOrigen = OrigenAltaForma(request.POST, prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(
            request.POST, prefix='origen')
        if has_info(request.POST, prefix='origen', investigacion=investigacion):
            if formOrigen.is_valid():
                origen = formOrigen.save(commit=False)
                origen.persona = investigacion.candidato
                origen.save()
            else:
                msg_param = ''
        ####################### Dirección #######################
        formDireccion = DireccionForm(request.POST, prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(
            request.POST, prefix='direccion')
        if has_info(request.POST, prefix='direccion', investigacion=investigacion):
            if formDireccion.is_valid():
                direccion = formDireccion.save(commit=False)
                direccion.persona = investigacion.candidato
                direccion.save()
            else:
                msg_param = ''
        ####################### Teléfono1 (casa)  #######################
        formTelefono1 = TelefonoForm(request.POST, prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(
            request.POST, prefix='telefono1')
        if has_info(request.POST, prefix='telefono1', investigacion=investigacion):
            if formTelefono1.is_valid():
                tel1 = formTelefono1.save(commit=False)
                tel1.persona = investigacion.candidato
                tel1.categoria = 'casa'
                tel1.save()
            else:
                msg_param = ''
        ####################### Teléfono2 (movil)  #######################
        formTelefono2 = TelefonoForm(request.POST, prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(
            request.POST, prefix='telefono2')
        if has_info(request.POST, prefix='telefono2', investigacion=investigacion):
            if formTelefono2.is_valid():
                tel2 = formTelefono2.save(commit=False)
                tel2.persona = investigacion.candidato
                tel2.categoria = 'movil'
                tel2.save()
            else:
                msg_param = ''
        ####################### Teléfono3 (recado)  #######################
        formTelefono3 = TelefonoForm(request.POST, prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(
            request.POST, prefix='telefono3')
        if has_info(request.POST, prefix='telefono3', investigacion=investigacion):
            if formTelefono3.is_valid():
                tel3 = formTelefono3.save(commit=False)
                tel3.persona = investigacion.candidato
                tel3.categoria = 'recado'
                tel3.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Infonavit #######################
        formPrestacionViviendaInfonavit = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit')
        if has_info(request.POST, prefix='prestacion_vivienda_infonavit', investigacion=investigacion):
            if formPrestacionViviendaInfonavit.is_valid():
                prestacionViviendaInfonavit = formPrestacionViviendaInfonavit.save(
                    commit=False)
                prestacionViviendaInfonavit.persona = investigacion.candidato
                prestacionViviendaInfonavit.categoria_viv = 'infonavit'
                prestacionViviendaInfonavit.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Fonacot #######################
        formPrestacionViviendaFonacot = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot')
        if has_info(request.POST, prefix='prestacion_vivienda_fonacot', investigacion=investigacion):
            if formPrestacionViviendaFonacot.is_valid():
                prestacionViviendaFonacot = formPrestacionViviendaFonacot.save(
                    commit=False)
                prestacionViviendaFonacot.persona = investigacion.candidato
                prestacionViviendaFonacot.categoria_viv = 'fonacot'
                prestacionViviendaFonacot.save()
            else:
                msg_param = ''
        ####################### Legalidad #######################
        formLegalidad = LegalidadAltaForma(
            request.POST, prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(request.POST, prefix='legalidad')
        if has_info(request.POST, prefix='legalidad', investigacion=investigacion):
            if formLegalidad.is_valid():
                legalidad = formLegalidad.save(commit=False)
                legalidad.persona = investigacion.candidato
                legalidad.save()
            else:
                msg_param = ''

        return redirect(reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id']}))


    def get_context_data(self, **kwargs):
        context = super(InvestigacionEjecutivoLaboralCandidatoTemplateView, self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.select_related(
            'compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        # agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        DemandaFormSet = modelformset_factory(
            Demanda, form=DemandaAltaForma, max_num=1, extra=1)

        context['title'] = "Investigaciones / Actualizacion datos del candidato"

        context['investigacion'] = investigacion

        context['formCandidato'] = CandidatoAltaForm(
            prefix='candidato', instance=investigacion.candidato)
        # context['formInvestigacion'] = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={
        #                                                        'compania': investigacion.compania.id}, agt_id=agente_id)
        context['formInvestigacion'] = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={
                                                               'compania': investigacion.compania.id})
        context['formOrigen'] = OrigenAltaForma(
            prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(prefix='origen')
        context['formDireccion'] = DireccionForm(
            prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(prefix='direccion')
        context['formTelefono1'] = TelefonoForm(
            prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(prefix='telefono1')
        context['formTelefono2'] = TelefonoForm(
            prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(prefix='telefono2')
        context['formTelefono3'] = TelefonoForm(
            prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(prefix='telefono3')
        context['formPrestacionViviendaInfonavit'] = PrestacionViviendaForma(
            prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit')
        context['formPrestacionViviendaFonacot'] = PrestacionViviendaForma(
            prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot')
        context['formLegalidad'] = LegalidadAltaForma(
            prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(prefix='legalidad')
        context['formDemanda'] = DemandaFormSet(
            queryset=Demanda.objects.filter(persona=investigacion.candidato))
        context['formSeguro'] = SeguroAltaForma(
            prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(prefix='seguro')
        context['formSucursal'] = CompaniaSucursalForm(
            investigacion.compania.id, investigacion.sucursal.id if investigacion.sucursal else None, prefix='investigacion')

        return context


class InvestigacionCoordinadorDemandasCreateView(CreateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Demanda
    fields = ['tiene_demanda', 'empresa', 'motivo',
              'ubicacion', 'fecha', 'audiencias', 'conclusion']
    template_name = 'investigaciones/demandas/demandas_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorDemandasCreateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.persona = inv.candidato
        self.object.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de Atenceon al clientei"
        bitacora.observaciones = "Creacion de demanda laboral"
        bitacora.save()

        return super(InvestigacionCoordinadorDemandasCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La demanada laboral se ha creado satisfactoriamente')
        return reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionCoordinadorDemandasUpdateView(UpdateView):

    # required
    group_required = u"Coord. de Atención a Clientes"
    raise_exception = True

    model = Demanda
    fields = ['tiene_demanda', 'empresa', 'motivo',
              'ubicacion', 'fecha', 'audiencias', 'conclusion']
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/demandas/demandas_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorDemandasUpdateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.save()

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Coordinador de visitas"
        bitacora.observaciones = "Actualizacion de demanda laboral"
        bitacora.save()

        return super(InvestigacionCoordinadorDemandasUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La demanda ha sido actualizado')
        return reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionCoordinadorDemandasDeleteView(GroupRequiredMixin, DeleteView):

    # required
    group_required = [u"Admin", u"Coord. de Atención a Clientes"]
    raise_exception = True

    model = Demanda
    template_name = 'investigaciones/demandas/demandas_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionCoordinadorDemandasDeleteView, self).get_context_data(**kwargs)

        context['investigacion'] = Investigacion.objects.get(
            id=self.kwargs['investigacion_id'])

        return context

     # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La demanda ha sido eliminado satisfactoriamente.')
        return reverse('investigaciones:investigacion_ejecutivo_laboral_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionCoordinadorCompletarTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Client", ]
    raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)

        cliente_solicitud_candidato = ClienteSolicitudCandidato.objects.get(pk=inv.cliente_solicitud_candidato_id)

        for csc in cliente_solicitud_candidato.tipo_investigacion.all():
            factura = InvestigacionFactura()
            factura.investigacion_id = investigacion_id
            #factura.cliente_solicitud_candidato_id = inv.cliente_solicitud_candidato_id
            factura.cantidad = 1
            factura.descripcion = csc
            factura.monto = csc.costo
            factura.save()

        cliente_solicitud_candidato.completado = True
        cliente_solicitud_candidato.factura_creada = True
        cliente_solicitud_candidato.save()
        
        inv.investigacion_completada = True
        inv.save()

        return redirect('investigaciones:investigacion_detail', self.kwargs['investigacion_id'])


class InvestigacionCoordinadorCompletarInvLaboralTemplateView(LoginRequiredMixin, TemplateView):

    # # required
    # group_required = [u"Client", ]
    # raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)
        
        inv.laboral_completado = True
        inv.save()

        return redirect('investigaciones:investigacion_detail', self.kwargs['investigacion_id'])


class InvestigacionCoordinadorCompletarEntrevistaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)
        
        inv.entrevista_from_completado = True
        inv.save()

        return redirect('investigaciones:investigaciones_entrevista_detail', seccion_entrevista='info_personal', investigacion_id=self.kwargs['investigacion_id'])
    

class InvestigacionCoordinadorCompletarAdjuntosTemplateView(LoginRequiredMixin, TemplateView):

    # # required
    # group_required = [u"Client", ]
    # raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)
        
        inv.entrevista_app_completado = True
        inv.save()

        return redirect('investigaciones:investigaciones_adjuntos_detail', self.kwargs['investigacion_id'])


class InvestigacionCobranzasCompletarFacturaTemplateView(LoginRequiredMixin, TemplateView):

    # # required
    # group_required = [u"Client", ]
    # raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)
        
        inv.investigacion_factura_completada = True
        inv.save()

        return redirect('cobranza_facturas_detail', self.kwargs['investigacion_id'])


class InvestigacionCobranzasClienteCompletaComprobanteTemplateView(LoginRequiredMixin, TemplateView):

    # # required
    # group_required = [u"Client", ]
    # raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):
        investigacion_id = self.kwargs['investigacion_id']
        inv = Investigacion.objects.get(id=investigacion_id)
        
        inv.investigacion_factura_pago_completado = True
        inv.save()

        return redirect('clientes:clientes_factura_detail', self.kwargs['investigacion_id'])