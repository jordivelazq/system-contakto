# -*- coding: utf-8 -*-

from app.clientes.models import ClienteSolicitudCandidato
from app.compania.models import DireccionFiscal
from app.investigacion.models import (
    Investigacion,
    InvestigacionFactura,
    InvestigacionFacturaArchivos,
    InvestigacionFacturaClienteArchivo,
)
from app.investigacion.serializers import InvestigacionSerializer

from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages


from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from rest_framework import mixins, viewsets


class InvestigacionFacturaTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    # model = Investigacion
    # paginate_by = 25

    context_object_name = "investigaciones_completadas"
    template_name = "cobranza/facturas/solicitudes_list.html"

    # def get_queryset(self):

    #     return Investigacion.objects.filter(investigacion_completada=True).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaTemplateView, self).get_context_data(
            **kwargs
        )

        context["title"] = "Cobranzas / Listado de facturas"
        # u = User.objects.get(id=self.request.user.pk)

        return context


class InvestigacionFacturaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):

        qs = self.queryset.filter(
            cliente_solicitud__isnull=False,
            # investigacion_completada=True
        ).order_by("last_modified")

        return qs


class InvestigacionFacturalDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = Investigacion
    context_object_name = "cliente_solicitud"
    template_name = "cobranza/facturas/solicitud_detail.html"

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturalDetailView, self).get_context_data(
            **kwargs
        )

        context["investigacion"] = Investigacion.objects.get(id=self.kwargs["pk"])

        context["title"] = "Cliente / Detalle de solicitud"

        context[
            "cliente_solicitud_candidatos_facturas"
        ] = InvestigacionFactura.objects.filter(investigacion=self.object)

        inv_factura_archivos = None
        try:
            inv_factura_archivos = InvestigacionFacturaArchivos.objects.get(
                investigacion=self.object
            )
        except InvestigacionFacturaArchivos.DoesNotExist:
            print("archivos no existe")

        # DEvuelve los datos de pagos del cliente
        inv_cliente_factura_archivos = (
            InvestigacionFacturaClienteArchivo.objects.filter(
                investigacion=self.object
            )
        )

        context["inv_factura_archivos"] = inv_factura_archivos
        context["inv_cliente_factura_archivos"] = inv_cliente_factura_archivos

        return context


class InvestigacionFacturaUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = InvestigacionFactura
    template_name = "cobranza/facturas/solicitud_form.html"
    fields = ["descuento"]

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaUpdateView, self).get_context_data(**kwargs)

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "El monto de descuento ha sido actualizado correctamente",
        )
        return reverse(
            "cobranza_facturas_detail", kwargs={"pk": self.kwargs["investigacion_id"]}
        )


class InvestigacionFacturaArchivosCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = InvestigacionFacturaArchivos
    fields = ("archivo_pdf", "archivo_xml")
    template_name = "cobranza/facturas/solicitud_archivos_form.html"

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaArchivosCreateView, self).get_context_data(
            **kwargs
        )

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.investigacion = Investigacion.objects.get(
            id=self.kwargs["investigacion_id"]
        )
        self.object.save()

        messages.add_message(
            self.request, messages.SUCCESS, "The user was created successfully"
        )

        return super(InvestigacionFacturaArchivosCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "Los archivos han sido creados"
        )
        return reverse(
            "cobranza_facturas_detail", kwargs={"pk": self.kwargs["investigacion_id"]}
        )


class InvestigacionFacturaArchivosUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = InvestigacionFacturaArchivos
    fields = ("archivo_pdf", "archivo_xml")
    template_name = "cobranza/facturas/solicitud_archivos_form.html"

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaArchivosUpdateView, self).get_context_data(
            **kwargs
        )

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        return context

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "Los archivos han sido actualizados"
        )
        return reverse(
            "cobranza_facturas_detail", kwargs={"pk": self.kwargs["investigacion_id"]}
        )


class InvestigacionFacturaDireccionFiscalUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = ClienteSolicitudCandidato
    fields = ("direccion_fiscal",)
    template_name = "cobranza/facturas/solicitud_cliente_candidato_form.html"

    def get_context_data(self, **kwargs):
        context = super(
            InvestigacionFacturaDireccionFiscalUpdateView, self
        ).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(id=self.kwargs["investigacion_id"])

        context["investigacion_id"] = self.kwargs["investigacion_id"]

        context["form"].fields[
            "direccion_fiscal"
        ].queryset = DireccionFiscal.objects.filter(
            compania_id=investigacion.compania_id
        )

        return context

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "La dirección fiscal ha sido actualizada"
        )
        return reverse(
            "cobranza_facturas_detail", kwargs={"pk": self.kwargs["investigacion_id"]}
        )


class InvestigacionFacturaClienteArchivoUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = ["Admin", "SuperAdmin", "Cobranzas"]
    raise_exception = True

    model = Investigacion
    template_name = "cobranza/facturas/aprobacion_comprobante_form.html"
    fields = ["investigacion_factura_pago_verificado"]

    def get_context_data(self, **kwargs):
        context = super(
            InvestigacionFacturaClienteArchivoUpdateView, self
        ).get_context_data(**kwargs)

        inv = Investigacion.objects.get(id=self.kwargs["investigacion_id"])

        try:
            inv_archivos = InvestigacionFacturaArchivos.objects.get(investigacion=inv)
        except InvestigacionFacturaClienteArchivo.DoesNotExist:
            inv_archivos = None

        context["investigacion_id"] = self.kwargs["investigacion_id"]
        context["inv_archivos"] = inv_archivos

        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "El comprobante de pago ha sido actualizado correctamente",
        )
        return reverse(
            "cobranza_facturas_detail", kwargs={"pk": self.kwargs["investigacion_id"]}
        )
