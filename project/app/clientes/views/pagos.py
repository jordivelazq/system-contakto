
# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from operator import inv

from app.adjuntos.models import Adjuntos
from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.investigacion.serializers import InvestigacionSerializer
from app.clientes.models import ClienteSolicitudCandidato
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
from rest_framework import mixins, viewsets
from utils.send_mails import send_email
from app.investigacion.models import Investigacion, InvestigacionFacturaClienteArchivo, InvestigacionFacturaArchivos


class ClientesFacturaTemplateView(LoginRequiredMixin, TemplateView):

    context_object_name = "investigaciones_completadas"
    template_name = 'clientes/facturas/facturas_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClientesFacturaTemplateView, self).get_context_data(**kwargs)

        context['title'] = "Cobranzas / Listado de facturas"

        return context


class ClientesFacturaDetailView(LoginRequiredMixin, DetailView):

    '''Detalle de pagos del cliente'''

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'clientes/facturas/facturas_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClientesFacturaDetailView, self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        try:
            cliente_factura = InvestigacionFacturaClienteArchivo.objects.get(investigacion=inv)
        except InvestigacionFacturaClienteArchivo.DoesNotExist:
            cliente_factura = None
        

        try:
            inv_archivos = InvestigacionFacturaArchivos.objects.get(investigacion=inv)
        except InvestigacionFacturaClienteArchivo.DoesNotExist:
            inv_archivos = None

        context['cliente_factura'] = cliente_factura
        context['investigacion_id'] = inv.id
        context['investigacion'] = inv
        context['inv_archivos'] = inv_archivos

        return context


class InvestigacionClienteFacturaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):

        # Buscar Cliente, 
        # filtar invistigaciones del cliente solicitudes del cliente
        qs = self.queryset.filter(
                 cliente_solicitud__isnull=False, investigacion_factura_completada=True).order_by("last_modified")

        return qs
    

class InvestigacionFacturaClienteArchivoCreateView(LoginRequiredMixin, CreateView):


    model = InvestigacionFacturaClienteArchivo
    fields = ['notas', 'fecha', 'comprobante'] 
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'clientes/facturas/facturas_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaClienteArchivoCreateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        return super(InvestigacionFacturaClienteArchivoCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El ejecutivo ha sido asignado')
        return reverse('clientes:clientes_factura_detail', kwargs={"pk": self.kwargs['investigacion_id']})


class InvestigacionFacturaClienteArchivoUpdateView(LoginRequiredMixin, UpdateView):


    model = InvestigacionFacturaClienteArchivo
    fields = ['notas', 'fecha', 'comprobante'] 
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'clientes/facturas/facturas_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionFacturaClienteArchivoUpdateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    # def form_valid(self, form):

    #     inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

    #     self.object = form.save(commit=False)
    #     self.object.investigacion = inv
    #     self.object.save()

    #     return super(InvestigacionFacturaClienteArchivoCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El ejecutivo ha sido asignado')
        return reverse('clientes:clientes_factura_detail', kwargs={"pk": self.kwargs['investigacion_id']})
