
# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from operator import inv

from app.adjuntos.models import Adjuntos
from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.investigacion.models import (Investigacion, InvestigacionFactura,
                                      InvestigacionFacturaArchivos,
                                      Psicometrico)
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


class ClientesFacturaTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    # model = Investigacion
    # paginate_by = 25

    context_object_name = "investigaciones_completadas"
    template_name = 'clientes/facturas/facturas_list.html'

    # def get_queryset(self):

    #     return Investigacion.objects.filter(investigacion_completada=True).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(ClientesFacturaTemplateView, self).get_context_data(**kwargs)

        context['title'] = "Cobranzas / Listado de facturas"
        # u = User.objects.get(id=self.request.user.pk)

        return context


class InvestigacionClienteFacturaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
    
        qs = self.queryset.filter(
                 cliente_solicitud__isnull=False, investigacion_factura_completada=True).order_by("last_modified")

        return qs