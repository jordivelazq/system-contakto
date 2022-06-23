from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import GestorInfo
from .serializers import GestorInfoSerializer


class GestorInfoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'agente/gestor_info_list.html'

    def get_context_data(self, **kwargs):
        context = super(GestorInfoTemplateView, self).get_context_data(**kwargs)

        return context


class GestorInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GestorInfo.objects.all()
    serializer_class = GestorInfoSerializer
