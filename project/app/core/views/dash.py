from app.clientes.models import ClienteUser, ClienteSolicitud
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from app.compania.models import Compania
from app.investigacion.models import Investigacion



class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        if self.request.user.groups.filter(name="Cliente").exists():

            cliente_solicitudes_total = ClienteSolicitud.objects.filter(
                cliente=self.request.user
            ).count()

            cliente_solicitudes_enviadas = ClienteSolicitud.objects.filter(
                cliente=self.request.user, enviado=True
            ).count()

            cliente_solicitudes_pendientes = ClienteSolicitud.objects.filter(
                cliente=self.request.user, enviado=False
            ).count()

            cliente = ClienteUser.objects.filter(pk=self.request.user.pk)
            if cliente:
                cliente = cliente.first()

            cliente_solicitud = ClienteSolicitud.objects.filter(
                cliente=cliente
            ).values_list("id", flat=True)

            total_facturas_por_pagar = Investigacion.objects.filter(
                cliente_solicitud__in=cliente_solicitud,
                investigacion_factura_enviada_al_cliente=True,
                investigacion_factura_pago_completado=False,
            ).count()

            total_facturas_pagadas = Investigacion.objects.filter(
                cliente_solicitud__in=cliente_solicitud,
                investigacion_factura_enviada_al_cliente=True,
                investigacion_factura_pago_completado=True,
            ).count()

            context["cliente_solicitudes_total"] = cliente_solicitudes_total
            context["cliente_solicitudes_enviadas"] = cliente_solicitudes_enviadas
            context["cliente_solicitudes_pendientes"] = cliente_solicitudes_pendientes
            context["total_facturas_por_pagar"] = total_facturas_por_pagar
            context["total_facturas_pagadas"] = total_facturas_pagadas
            context["is_cliente"] = 1

        if self.request.user.groups.filter(
            name="Coord. de Atención a Clientes"
        ).exists():

            companias_pk = Compania.objects.filter(
                coordinador_ejecutivos_id=user.pk
            ).values_list("pk", flat=True)

            total_investigaciones = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk
            ).count()

            print(total_investigaciones, "total_investigaciones")

            en_investigacion = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=0
            ).count()

            pte_por_el_cliente = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=1
            ).count()

            inv_terminada = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=2
            ).count()

            context["total_investigaciones"] = total_investigaciones
            context["en_investigacion"] = en_investigacion
            context["pte_por_el_cliente"] = pte_por_el_cliente
            context["inv_terminada"] = inv_terminada
            context["coord_de_atencion_a_clientes"] = 1

            print(
                "Totales",
                total_investigaciones,
                en_investigacion,
                pte_por_el_cliente,
                inv_terminada,
            )

        if self.request.user.groups.filter(name="Cobranzas").exists():

            facturas_a_enviar = Investigacion.objects.filter(
                cliente_solicitud__isnull=False
            ).count()

            pagos_por_validar = Investigacion.objects.filter(
                cliente_solicitud__isnull=False
            ).count()

            facturas_por_generar = Investigacion.objects.filter(
                cliente_solicitud__isnull=False
            ).count()

            context["facturas_a_enviar"] = (facturas_a_enviar,)
            context["pagos_por_validar"] = (pagos_por_validar,)
            context["facturas_por_generar"] = (facturas_por_generar,)
            # context["inv_terminada"] = inv_terminada,

        return context
