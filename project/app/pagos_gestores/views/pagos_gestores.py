# -*- coding: utf-8 -*-

import json
from datetime import date, datetime
from operator import inv

from app.adjuntos.models import Adjuntos
from app.agente.models import GestorInfo
from app.clientes.models import ClienteSolicitudCandidato
from app.compania.models import DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio, UserMessage
from app.entrevista.entrevista_persona import EntrevistaPersonaService
from app.investigacion.models import (GestorInvestigacion,
                                      GestorInvestigacionPago,
                                      GestorInvestigacionPagoInv,
                                      Investigacion, InvestigacionBitacora,
                                      InvestigacionFacturaArchivos,
                                      InvestigacionFacturaClienteArchivo)
from app.investigacion.serializers import (GestorInfoSerializer,
                                           GestorInvestigacionPagoSerializer,
                                           GestorInvestigacionSerializer,
                                           InvestigacionSerializer)
from app.persona.models import Persona, Telefono
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
from rest_framework import mixins, viewsets
from utils.send_mails import send_email



class GestoresInvestigacionListView(LoginRequiredMixin, ListView):

    context_object_name = "investigaciones_pagos_pendientes"
    template_name = 'pagos/gestores/pendientes/pagos2_list.html'
    model = GestorInvestigacion

    def get_queryset(self):
        qs = GestorInvestigacion.objects.filter(completado=True, pagado=False).values('gestor', 'completado')\
                                        .annotate(gcount=Count('gestor')).order_by('-gcount')
        return qs

    def get_context_data(self, **kwargs):
        context = super(GestoresInvestigacionListView, self).get_context_data(**kwargs)

        context['title'] = "Pagos / Listado de de pagos pendientes"

        return context


class GestoresInvestigacionDetsilTemplateView(LoginRequiredMixin, TemplateView):

    context_object_name = "investigaciones_completadas"
    template_name = 'pagos/gestores/pendientes/pagos_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GestoresInvestigacionDetsilTemplateView, self).get_context_data(**kwargs)

        context['title'] = "Pagos / Detalle de pago pendientes"

        gestor = GestorInfo.objects.get(id=kwargs['gestor_id'])
        inv_a_pagar = GestorInvestigacion.objects.filter(gestor=gestor, pagado=False, completado=True)

        context['gestor'] = gestor
        context['inv_a_pagar'] = inv_a_pagar
        context['gestor_id'] = kwargs['gestor_id']

        return context


class GenerarPagoGestorTemplateView(LoginRequiredMixin, TemplateView):

    # # required
    # group_required = [u"Client", ]
    # raise_exception = True

    template_name = ''

    def get(self, request, **kwargs):

        gestor = GestorInfo.objects.get(id=kwargs['gestor_id'])
        inv_a_pagar = GestorInvestigacion.objects.filter(gestor=gestor, pagado=False, completado=True)

        # Genera pago al gestor
        gip = GestorInvestigacionPago.objects.create(gestor=gestor,)

        inv_a_pagar = GestorInvestigacion.objects.filter(gestor=gestor, pagado=False, completado=True)

        # genera respaldo
        for iap in inv_a_pagar:
            iap.pagado=True
            iap.save()
            print
            gipi = GestorInvestigacionPagoInv.objects.create(gestor_investigacion_pago=gip, investigacion=iap.investigacion)
            # gipi.save()

       
        return HttpResponseRedirect('/pagos_a_gestores/pago/update/'+str(gip.pk)+'/')


class GestorInvestigacionPagoUpdateView(LoginRequiredMixin, UpdateView):

    model = GestorInvestigacionPago
    fields = ['fecha_de_pago', 'comprobante']
    template_name = 'pagos/gestores/pendientes/pagos_form.html'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.pagado = True
        self.object.save()

        gestor = GestorInfo.objects.get(id=self.object.gestor.id)

        # se debe generar un mensaje por cada investigacion pagada
        # bitacora = InvestigacionBitacora()
        # bitacora.user_id = self.request.user.pk
        # bitacora.investigacion = inv
        # bitacora.servicio = "Ejecutivo de pago"
        # bitacora.observaciones = "ha generado pago a gestor"
        # bitacora.save()

        # Genera mensaje a usuario
        msj = UserMessage()
        msj.user = gestor.usuario

        msj.title = "Se ha generado un pago por gestorías"
        msj.message = "Estimado usuario. Se ha registrado un pafo gestoris"
        msj.link = "/investigaciones/investigaciones/coordinador-visitas/detail/" +  str(self.object.pk)+"/"
        msj.save()

        return super(GestorInvestigacionPagoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GestorInvestigacionPagoUpdateView, self).get_context_data(**kwargs)

        context['title'] = "Pagos / Formulario de pago a gestores"

        return context

    def get_success_url(self):
        return reverse('pagos_gestores:pagos_gestores_list')


class GestorInvestigacionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = GestorInfo.objects.all()
    # serializer_class = GestorInfoSerializer
    queryset = GestorInvestigacion.objects.all()
    serializer_class = GestorInvestigacionSerializer

    def get_queryset(self):

        # Buscar Cliente, 
        # filtar invistigaciones del cliente solicitudes del cliente
        
        qs = self.queryset.filter(compleado=True, pagado=False).values("gestor", ).annotate(gcount=Count('gestor', distinct=True))
       
        # qs = self.queryset.filter(compleado=True, pagado=False).values("gestor", ).aggregate(total_inv=Count("gestor"))
        # qs = self.queryset.filter(compleado=True, pagado=False).aggregate(total_inv=Count("gestor"))
        # qs = self.queryset.filter(compleado=True, pagado=False).values("gestor", ).aggregate(gcount=Count('gestor'))
        # qs = self.queryset.filter(compleado=True, pagado=False).annotate(gcount=Count('gestor', distinct=True))
        # qs = self.queryset.filter(compleado=True, pagado=False).annotate(total_inv=Count('gestor'))

        return qs


class GestorInvestigacionPagoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = GestorInvestigacionPago.objects.all()
    serializer_class = GestorInvestigacionPagoSerializer


class GestoresInvestigacionPagosInvTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'pagos/gestores/pagados/pagos_list.html'

    def get_context_data(self, **kwargs):
        context = super(GestoresInvestigacionPagosInvTemplateView, self).get_context_data(**kwargs)

        context['title'] = "Pagos / Listado de pagos efectuados"

        return context