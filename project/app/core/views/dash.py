from app.clientes.models import ClienteSolicitud
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from app.compania.models import Compania
from app.investigacion.models import Investigacion


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

            context = {
                "cliente_solicitudes_total": cliente_solicitudes_total,
                "cliente_solicitudes_enviadas": cliente_solicitudes_enviadas,
                "cliente_solicitudes_pendientes": cliente_solicitudes_pendientes,
            }

        if self.request.user.groups.filter(name="Coord. de Atención a Clientes").exists():

            user = self.request.user
            companias_pk = Compania.objects.filter(
                coordinador_ejecutivos_id=user.pk
            ).values_list("pk", flat=True)

            total_investigaciones = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk
            ).count()

            en_investigacion = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=0
            ).count()

            pte_por_el_cliente = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=1
            ).count()

            inv_terminada = Investigacion.objects.filter(
                cliente_solicitud__isnull=False, compania__in=companias_pk, status=2
            ).count()

            context = {
                "total_investigaciones": total_investigaciones,
                "en_investigacion": en_investigacion,
                "pte_por_el_cliente": pte_por_el_cliente,
                "inv_terminada": inv_terminada,
            }

        return context
