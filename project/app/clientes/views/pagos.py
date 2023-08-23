# -*- coding: utf-8 -*-

from app.investigacion.models import (
    Investigacion,
    InvestigacionFacturaArchivos,
    InvestigacionFactura,
    InvestigacionFacturaClienteArchivo,
)
from app.clientes.models import ClienteUser, ClienteSolicitud
from app.investigacion.serializers import InvestigacionSerializer
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from rest_framework import mixins, viewsets
from utils.general_utils import CreateGroupMessajeInd


class ClientesFacturaTemplateView(LoginRequiredMixin, TemplateView):

    context_object_name = "investigaciones_completadas"
    template_name = "clientes/facturas/facturas_list.html"

    def get_context_data(self, **kwargs):
        context = super(ClientesFacturaTemplateView, self).get_context_data(**kwargs)

        context["title"] = "Cobranzas / Listado de facturas"

        return context


class ClientesFacturaDetailView(LoginRequiredMixin, DetailView):

    """Detalle de pagos del cliente"""

    model = Investigacion
    context_object_name = "investigacion"
    template_name = "clientes/facturas/facturas_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClientesFacturaDetailView, self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs["pk"])

        try:
            cliente_factura = InvestigacionFacturaArchivos.objects.get(
                investigacion=inv
            )
        except InvestigacionFacturaArchivos.DoesNotExist:
            cliente_factura = None

        context[
            "cliente_solicitud_candidatos_facturas" 
        ] = InvestigacionFactura.objects.filter(investigacion=self.object)

        inv_cliente_factura_archivos = InvestigacionFacturaClienteArchivo.objects.filter(investigacion=inv)

        context["cliente_factura"] = cliente_factura
        context["investigacion_id"] = inv.id
        context["investigacion"] = inv
        context["inv_cliente_factura_archivos"] = inv_cliente_factura_archivos

        return context


class InvestigacionClienteFacturaViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):

        # Buscar Cliente,

        cliente = ClienteUser.objects.get(pk=self.request.user.pk)

        cliente_solicitud = ClienteSolicitud.objects.filter(
            cliente=cliente
        ).values_list("id", flat=True)

        qs = self.queryset.filter(
            cliente_solicitud__in=cliente_solicitud,
            investigacion_factura_enviada_al_cliente=True,
        ).order_by("last_modified")

        return qs


class InvestigacionFacturaClienteArchivoCreateView(LoginRequiredMixin, CreateView):

    model = InvestigacionFacturaClienteArchivo
    fields = ["fecha", "monto", "notas", "comprobante"]
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = "clientes/facturas/facturas_form.html"

    def get_context_data(self, **kwargs):
        context = super(
            InvestigacionFacturaClienteArchivoCreateView, self
        ).get_context_data(**kwargs)

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs["investigacion_id"])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        # Enviar mensaje a cobranzas
        group_name = "Cobranzas"
        investigacion_id = inv.id
        title = "Cliente ha generado un nuevo comprobante de pago"
        message = "El cliente ha generado un nuevo comprobante de pago para la investigación: {}".format(
            inv.id
        )
        link = "/cobranza/facturas/detail/{}/".format(inv.id)

        CreateGroupMessajeInd().create_group_message(group_name, investigacion_id, title, message, link)

        return super(InvestigacionFacturaClienteArchivoCreateView, self).form_valid(
            form
        )

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "El ejecutivo ha sido asignado"
        )
        return reverse(
            "clientes:clientes_factura_detail",
            kwargs={"pk": self.kwargs["investigacion_id"]},
        )


class InvestigacionFacturaClienteArchivoUpdateView(LoginRequiredMixin, UpdateView):

    model = InvestigacionFacturaClienteArchivo
    fields = ["fecha", "monto", "notas", "comprobante"]
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = "clientes/facturas/facturas_form.html"

    def get_context_data(self, **kwargs):
        context = super(
            InvestigacionFacturaClienteArchivoUpdateView, self
        ).get_context_data(**kwargs)

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "El ejecutivo ha sido asignado"
        )
        return reverse(
            "clientes:clientes_factura_detail",
            kwargs={"pk": self.kwargs["investigacion_id"]},
        )
