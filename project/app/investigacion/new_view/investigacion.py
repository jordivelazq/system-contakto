
# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    UpdateView
)

from app.investigacion.models import Investigacion


class InvestigacionCerrarUpdateView(LoginRequiredMixin, UpdateView):

    # required
    group_required = [u"Coord. de Atención a Clientes", u"Coordinador de visitas domiciliarias"]
    raise_exception = True

    model = Investigacion
    fields = ['resultado', 'conclusiones', 'observaciones']
    template_name = 'investigaciones/investigacion_update_form.html'

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS,
            'El Investigación ha sido actualizado satisfactoriamente.')
        return reverse(
            'investigaciones:investigacion_detail',
            kwargs={"pk": self.kwargs['pk']}
        )
