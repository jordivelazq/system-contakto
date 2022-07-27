from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from app.investigacion.models import Investigacion
from app.investigacion.serializers import InvestigacionSerializer


class EntrevistasTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'entrevistas/entrevistas_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntrevistasTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Companias'

        return context


class EntrevistaInvestigacionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
    
        qs = self.queryset.filter(
                 cliente_solicitud__isnull=False, agente=self.request.user ).order_by("last_modified")

        return qs