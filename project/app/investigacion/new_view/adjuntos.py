from multiprocessing import context

from app.compania.forms import *
from app.compania.models import Compania
from app.entrevista.services import *
from app.investigacion.forms import *
from app.persona.form_functions import *
from app.persona.forms import *
from app.persona.models import *
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from certifi import contents
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework import mixins, viewsets
from utils.general_utils import GetDataTime
from utils.send_mails import send_email

from ..models import (GestorInvestigacion, Investigacion, InvestigacionBitacora,
                     Psicometrico)
from ..serializers import InvestigacionSerializer

from app.adjuntos.models import Adjuntos

from app.adjuntos.forms import AdjuntosForm


class InvestigacionAdjuntosTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/adjuntos/investigaciones_adjuntos_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionAdjuntosTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones adjuntos'

        return context


class InvestigacionAdjuntosViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        
        user = self.request.user
        companias_pk = Compania.objects.filter(coordinador_ejecutivos_id=user.pk).values_list('pk', flat=True)

        # try:
        #     qs = self.queryset.filter(
        #         cliente_solicitud__isnull=False,compania__in=companias_pk ).order_by("last_modified")
        # except Compania.DoesNotExist:
        #     return self.queryset.none()
        
        qs = self.queryset.filter(
                 cliente_solicitud__isnull=False ).order_by("last_modified")

        return qs


class InvestigacionAdjuntosDetailView(DetailView):

    '''Detalle general para el Coorsinador de visitas'''

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/adjuntos/investigaciones_adjuntos_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionAdjuntosDetailView, self).get_context_data(**kwargs)
        
        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        adjuntos = Adjuntos.objects.filter(investigacion=inv)[0]
        context['adjuntos'] = adjuntos
       
        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=inv, user_id=self.request.user.pk).order_by('-datetime')

        return context


class InvestigacionAdjuntosFormTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/adjuntos/investigaciones_adjuntos_form.html'

    def post(self, request, *args, **kwargs):
       
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else Adjuntos(investigacion=investigacion)

   
        adjuntos_form = AdjuntosForm(request.POST, request.FILES, instance=adjuntos)
        if adjuntos_form.is_valid():
            adjuntos_form.save()
            return HttpResponseRedirect('/investigaciones/investigaciones/adjuntos/detail/' + str(self.kwargs['investigacion_id']))

    def get_context_data(self, **kwargs):
        context = super(InvestigacionAdjuntosFormTemplateView, self).get_context_data(**kwargs)
        #seccion_entrevista = self.kwargs['seccion_entrevista']
        
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        adjuntos = investigacion.adjuntos_set.all()[0] if investigacion.adjuntos_set.all().count() else Adjuntos(investigacion=investigacion)

        adjuntos_form = AdjuntosForm(instance=adjuntos)

        context['adjuntos_form'] = adjuntos_form

        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=investigacion, user_id=self.request.user.pk).order_by('-datetime')


        return context
    