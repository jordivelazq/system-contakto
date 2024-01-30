from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import ClienteSolicitud, ClienteUser
from .serializers import ClienteSolicitudSerializer, ClienteUserSerializer
from ..compania.models import Compania
from ..investigacion.models import Investigacion
from ..investigacion.serializers import InvestigacionSerializer


class ClienteTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/clientes_users/clientes_users_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class ClienteUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ClienteUser.objects.all()
    serializer_class = ClienteUserSerializer


class ClienteSolicitudViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ClienteSolicitud.objects.all()
    serializer_class = ClienteSolicitudSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            user=self.request.user).order_by("last_modified")

        return qs


class InvestigacionClienteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        cliente_solicitud = ClienteSolicitud.objects.filter(cliente=self.request.user)
        try:
            qs = self.queryset.filter(cliente_solicitud__in=cliente_solicitud).order_by("last_modified")
        except ClienteSolicitud.DoesNotExist:
            return self.queryset.none()
        return qs
class InvestigacionClienteEmpresaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        cliente_solicitud = ClienteSolicitud.objects.filter(cliente__compania=self.request.user.clienteuser.compania)
        try:
            qs = self.queryset.filter(cliente_solicitud__in=cliente_solicitud).order_by("last_modified")
        except ClienteSolicitud.DoesNotExist:
            return self.queryset.none()
        return qs

class CandidatosTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/candidato/candidato_investigacion_list.html'

    def get_context_data(self, **kwargs):
        context = super(CandidatosTemplateView, self).get_context_data(**kwargs)
        cliente_solicitud = ClienteSolicitud.objects.filter(cliente=self.request.user)
        total_investigaciones = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud
        ).count()

        en_investigacion = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=0
        ).count()

        pte_por_el_cliente = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=1
        ).count()

        inv_terminada = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=2
        ).count()
        context['title'] = 'Candidatos'
        context['total_investigaciones'] =total_investigaciones
        context['en_investigacion'] = en_investigacion
        context['pte_por_el_cliente'] =pte_por_el_cliente
        context['inv_terminada'] = inv_terminada
        return context

class CandidatosEmpresaTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes/candidato/candidato_investigacion_empresa_list.html'

    def get_context_data(self, **kwargs):
        context = super(CandidatosEmpresaTemplateView, self).get_context_data(**kwargs)
        cliente_solicitud = ClienteSolicitud.objects.filter(cliente__compania=self.request.user.clienteuser.compania)
        total_investigaciones = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud
        ).count()

        en_investigacion = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=0
        ).count()

        pte_por_el_cliente = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=1
        ).count()

        inv_terminada = Investigacion.objects.filter(
            cliente_solicitud__in=cliente_solicitud, status=2
        ).count()
        context['title'] = 'Candidatos'
        context['total_investigaciones'] =total_investigaciones
        context['en_investigacion'] = en_investigacion
        context['pte_por_el_cliente'] =pte_por_el_cliente
        context['inv_terminada'] = inv_terminada
        return context

