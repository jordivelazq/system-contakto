from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import Persona
from .serializers import PersonaSerializer


class PersonasTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'personas/personas_list.html'

    def get_context_data(self, **kwargs):
        context = super(PersonasTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class PersonaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
