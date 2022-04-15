from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.agente.forms import UserPerfilUpdate


class PerfilUpdateView(UpdateView):
    model = User
    form_class = UserPerfilUpdate
    template_name = 'sections/agente/perfil_form.html'

    def get_context_data(self, **kwargs):
        context = super(PerfilUpdateView, self).get_context_data(**kwargs)
        context['page'] = 'perfil'
        context['title'] = 'Actualización de perfil'
        context['msg_class'] = 'alert alert-danger'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente.')
        return super(PerfilUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'No se completó el proceso, inténtelo nuevamente.')
        return super(PerfilUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('perfil-update', kwargs={'pk': self.object.id})
