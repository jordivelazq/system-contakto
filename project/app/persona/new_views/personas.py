from django.urls import reverse_lazy
from ..models import Persona
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib import messages
from django.urls import reverse, reverse_lazy


class PersonaDetailView(DetailView):
    model = Persona
    template_name = 'personas/persona/persona_detail.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Compañia'
        return context
