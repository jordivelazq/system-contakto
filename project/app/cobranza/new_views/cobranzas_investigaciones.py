

# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from operator import inv

from app.adjuntos.models import Adjuntos

from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.investigacion.models import Investigacion, Psicometrico, InvestigacionFactura, InvestigacionFacturaArchivos
from app.persona.models import Persona, Telefono
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
from utils.send_mails import send_email


class InvestigacionFacturaListView(GroupRequiredMixin, ListView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = Investigacion
    paginate_by = 25

    context_object_name = "investigaciones_completadas"
    template_name = 'cobranza/facturas/solicitudes_list.html'

    def get_queryset(self):

        return Investigacion.objects.filter(investigacion_completada=True).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaListView, self).get_context_data(**kwargs)

        context['title'] = "Cobranzas / Listado de facturas"
        u = User.objects.get(id=self.request.user.pk)

        return context



class InvestigacionFacturalDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = [u"Client", u"SuperAdmin"]
    raise_exception = True

    model = Investigacion
    context_object_name = "cliente_solicitud"
    template_name = 'cobranza/facturas/solicitud_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturalDetailView, self).get_context_data(**kwargs)

        context['title'] = "Cliente / Detalle de solicitud"

        context['cliente_solicitud_candidatos_facturas'] = InvestigacionFactura.objects.filter(investigacion=self.object)

        inv_factura_archivos = None
        try:
            inv_factura_archivos = InvestigacionFacturaArchivos.objects.get(investigacion=self.object)
        except InvestigacionFacturaArchivos.DoesNotExist:
            print('archivos no existe')

        context['inv_factura_archivos'] = inv_factura_archivos
        
        return context


class InvestigacionFacturaUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = InvestigacionFactura
    template_name = 'cobranza/facturas/solicitud_form.html'
    fields = ['descuento']

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaUpdateView, self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']
        
        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El monto de descuento ha sido actualizado correctamente')
        return reverse('cobranza_facturas_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionFacturaArchivosCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = InvestigacionFacturaArchivos
    fields = ('archivo_pdf', 'archivo_xml')
    template_name = 'cobranza/facturas/solicitud_archivos_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaArchivosCreateView, self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        self.object.save()
       
        messages.add_message(self.request, messages.SUCCESS, 'The user was created successfully')

        return super(InvestigacionFacturaArchivosCreateView, self).form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Los archivos han sido creados')
        return reverse('cobranza_facturas_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionFacturaArchivosUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = InvestigacionFacturaArchivos
    fields = ('archivo_pdf', 'archivo_xml')
    template_name = 'cobranza/facturas/solicitud_archivos_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaArchivosUpdateView, self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']
        
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Los archivos han sido actualizados')
        return reverse('cobranza_facturas_detail', kwargs={"pk": self.kwargs['investigacion_id']})