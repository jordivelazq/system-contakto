# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from operator import inv

from app.adjuntos.models import Adjuntos
from app.clientes.models import (
    Cliente,
    ClienteSolicitud,
    ClienteSolicitudCandidato,
    ClienteTipoInvestigacion,
    ClienteUser,
)
from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.investigacion.models import (
    Investigacion,
    Psicometrico,
    InvestigacionFacturaClienteArchivo,
)
from app.persona.models import Persona, Telefono
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from utils.send_mails import send_email


class ClienteSolicitudesCanditatosFacturasListView(GroupRequiredMixin, ListView):

    # required
    group_required = ["Admin", "SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitud
    paginate_by = 25

    context_object_name = "cliente_solicitudes"
    template_name = "cobranza/facturas/solicitudes_list.html"

    def get_queryset(self):

        return ClienteSolicitud.objects.filter().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(
            ClienteSolicitudesCanditatosFacturasListView, self
        ).get_context_data(**kwargs)

        context["title"] = "Cobranzas / Listado de facturas"
        u = User.objects.get(id=self.request.user.pk)

        return context


# class ClienteSolicitudDetaiFacturalView(GroupRequiredMixin, DetailView):

#     # required
#     group_required = ["Client", "SuperAdmin"]
#     raise_exception = True

#     model = ClienteSolicitud
#     context_object_name = "cliente_solicitud"
#     template_name = "cobranza/facturas/solicitud_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super(ClienteSolicitudDetaiFacturalView, self).get_context_data(
#             **kwargs
#         )

#         context["title"] = "Cliente / Detalle de solicitud"

#         context[
#             "cliente_solicitud_candidatos_facturas"
#         ] = ClienteSolicitudFactura.objects.filter(cliente_solicitud=self.object)

#         return context


# class ClienteSolicitudFacturaUpdateView(GroupRequiredMixin, UpdateView):

#     # required
#     group_required = ["Admin", "SuperAdmin"]
#     raise_exception = True

#     model = ClienteSolicitudFactura
#     template_name = "cobranza/facturas/solicitud_form.html"
#     fields = ["descuento"]

#     def get_context_data(self, **kwargs):
#         context = super(ClienteSolicitudFacturaUpdateView, self).get_context_data(
#             **kwargs
#         )

#         context["solicitud_id"] = self.kwargs["solicitud_id"]

#         return context

#     # send the user back to their own page after a successful update
#     def get_success_url(self, **kwargs):
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             "El monto de descuento ha sido actualizado correctamente",
#         )
#         return reverse(
#             "cobranza_facturas_detail", kwargs={"pk": self.kwargs["solicitud_id"]}
#         )


class InvestigacionFacturaClienteArchivopdateView(LoginRequiredMixin, UpdateView):

    model = InvestigacionFacturaClienteArchivo
    fields = ["verificado_por_cobranzas"]
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = "cobranza/facturas/solicitud_verificar_pago_form.html"

    def get_context_data(self, **kwargs):
        context = super(
            InvestigacionFacturaClienteArchivopdateView, self
        ).get_context_data(**kwargs)

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "El ejecutivo ha sido asignado"
        )
        return reverse(
            "cobranza_facturas_detail",
            kwargs={"pk": self.kwargs["investigacion_id"]},
        )
