# -*- coding: utf-8 -*-
from app.clientes.models import (
    ClienteSolicitud,
)

from app.investigacion.models import (
    Investigacion,
    InvestigacionFacturaClienteArchivo,
)


from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User


from django.urls import reverse
from django.views.generic import (
    ListView,
    UpdateView,
)
from app.core.models import UserMessage


class ClienteSolicitudesCanditatosFacturasListView(GroupRequiredMixin, ListView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
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

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs["investigacion_id"])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        msj = UserMessage()
        msj.user = inv.cliente_solicitud.cliente

        msj.title = "Su pago ha sido verificado por cobranza"
        msj.message = "Su pago ha sido verificado por cobranza, le invitamos a revisar su estado de cuenta"
        msj.link = "/clientes/facturas/detail/" + str(inv.pk) + "/"
        msj.save()

        return super(InvestigacionFacturaClienteArchivopdateView, self).form_valid(form)

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
