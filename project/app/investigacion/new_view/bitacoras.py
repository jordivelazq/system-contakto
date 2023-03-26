
# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
)

from app.investigacion.models import InvestigacionBitacora


class InvestigacionBitacoraCreateView(LoginRequiredMixin, CreateView):

    # required
    # group_required = u"Cliente"
    # raise_exception = True

    model = InvestigacionBitacora
    fields = ['observaciones']
    template_name = 'investigaciones/bitcoras/bitacora_form.html'

    def form_valid(self, form):

        servicio = "Investigacion"

        if self.kwargs['page'] == 'coord_serv_cliente':
            servicio = "Coordinador de atención al cliente"

        if self.kwargs['page'] == 'coord_eject_cuenta':
            servicio = "Ejecutivo de cuentas"

        if self.kwargs['page'] == 'eject_visita':
            servicio = "Ejecutivo de visitas"

        if self.kwargs['page'] == 'coord_visita_domiciliaria':
            servicio = "Coordinador de visitas domiciliarias"
        
        if self.kwargs['page'] == 'coord_entrevista':
            servicio = "Enrevisita"
        
        if self.kwargs['page'] == 'eject_psicometrico':
            servicio = "Ejecutivo psicometrico"

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.servicio = servicio
        self.object.investigacion_id = self.kwargs['investigacion_id']
        self.object.save()

        # super(InvestigacionBitacoraCreateView, self).form_valid(form)

        return super(InvestigacionBitacoraCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS,
            _('La bitacora fue creada correctamente'))

        if self.kwargs['page'] == 'coord_serv_cliente':
            return reverse(
                'investigaciones:investigacion_detail',
                kwargs={"pk": self.kwargs['investigacion_id']}
            )

        if self.kwargs['page'] == 'coord_eject_cuenta':
            return reverse(
                'investigaciones:investigacion_ejecutivo_laboral_detail',
                kwargs={"pk": self.kwargs['investigacion_id']}
            )

        if self.kwargs['page'] == 'eject_visita':
            return reverse(
                'investigaciones:investigaciones_ejecutivo_visitas_detail',
                kwargs={"pk": self.kwargs['investigacion_id'], 
                        "seccion_entrevista": "datos_generales"}
            )

        if self.kwargs['page'] == 'coord_visita_domiciliaria':
            return reverse(
                'investigaciones:investigaciones_coordinador_visitas_detail',
                kwargs={"pk": self.kwargs['investigacion_id']}
            )

        if self.kwargs['page'] == 'coord_entrevista':
            return reverse(
                'investigaciones:investigaciones_entrevista_detail',
                kwargs={
                        "seccion_entrevista": "datos_generales",        
                        "investigacion_id": self.kwargs['investigacion_id'],
                        }
            )
        
        if self.kwargs['page'] == 'coord_entrevista':
            return reverse(
                'investigaciones:investigaciones_entrevista_detail',
                kwargs={
                    "investigacion_id": self.kwargs['investigacion_id'],
                }
            )
        
        if self.kwargs['page'] == 'eject_psicometrico':
            return reverse(
                'investigaciones:investigaciones_coordinador_psicometrico_detail',
                kwargs={
                    "pk": self.kwargs['investigacion_id'],
                }
            )

    def get_context_data(self, **kwargs):
        context = super(InvestigacionBitacoraCreateView, self).get_context_data(**kwargs)

        if self.kwargs['page'] == 'coord_serv_cliente':
            context['page_title'] = 'Coordinador de atención al cliente'

        if self.kwargs['page'] == 'coord_eject_cuenta':
            context['page_title'] = 'Ejecutivo de cuentas'

        if self.kwargs['page'] == 'eject_visita':
            context['page_title'] = 'Ejecutivo de visitas'
        
        if self.kwargs['page'] == 'coord_visita_domiciliaria':
            context['page_title'] = 'Coordinador de visitas domiciliarias'

        if self.kwargs['page'] == 'coord_entrevista':
            context['page_title'] = 'Coordinador de entrevista'
        
        if self.kwargs['page'] == 'eject_psicometrico':
            context['page_title'] = 'Ejecutivo psicometrico'

        context['investigacion_id'] = self.kwargs['investigacion_id']
        return context
