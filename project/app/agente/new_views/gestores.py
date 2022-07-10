
from django.urls import reverse_lazy
from ..models import GestorInfo
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib import messages
from django.urls import reverse, reverse_lazy


class GestorInfoCreateView(CreateView):
    model = GestorInfo
    template_name = 'agente/gestor_form.html'
    fields = ('__all__')
    success_url = reverse_lazy('gestor_info_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear agente'
        return context


class GestorInfoUpdateView(UpdateView):
    model = GestorInfo
    template_name = 'agente/gestor_form.html'
    fields = ('__all__')
    success_url = reverse_lazy('gestor_info_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Compañia'
        context['compania_id'] = self.kwargs['pk']
        return context


class GestorInfoDeleteView(DeleteView):
    model = GestorInfo
    context_object_name = 'gestor_info'
    template_name = 'agente/gestor_delete.html'
    success_url = reverse_lazy('gestor_info_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Agentes'
        return context
