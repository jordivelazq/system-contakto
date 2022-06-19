from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import Compania
from .serializers import CompaniaSerializer


class CompaniaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'companias/companias_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompaniaTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Companias'

        return context


class CompaniaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Compania.objects.all()
    serializer_class = CompaniaSerializer
