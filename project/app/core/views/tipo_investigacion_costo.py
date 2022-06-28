
# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from ..models import TipoInvestigacionCosto


class TipoInvestigacionCostoListView(GroupRequiredMixin, ListView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = TipoInvestigacionCosto
    context_object_name = 'tipo_investigacion_costo_list'
    paginate_by = 25

    template_name = 'core/tipo_investigacion_costo/tipo_investigacion_costo_list.html'

    page = {
        'title': 'Projects',
        'subtitle': 'list'
    }

    def get_context_data(self, **kwargs):
        context = super(TipoInvestigacionCostoListView,
                        self).get_context_data(**kwargs)

        context['page'] = self.page

        return context


class TipoInvestigacionCostoCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = TipoInvestigacionCosto

    fields = [
        'tipo_investigacion', 'costo',
    ]
    template_name = 'core/tipo_investigacion_costo/tipo_investigacion_costo_form.html'

    def get_context_data(self, **kwargs):
        context = super(TipoInvestigacionCostoCreateView,
                        self).get_context_data(**kwargs)

        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Costo de la investigación ha sido creado')
        return reverse('core:tipo_investigaciones_costo_list')


class TipoInvestigacionCostoUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = TipoInvestigacionCosto
    context_object_name = "projects"

    fields = [
        'tipo_investigacion', 'costo',
    ]
    template_name = 'core/tipo_investigacion_costo/tipo_investigacion_costo_form.html'

    def get_context_data(self, **kwargs):
        context = super(TipoInvestigacionCostoUpdateView,
                        self).get_context_data(**kwargs)

        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Costo de la investigación ha sido actualizado')
        return reverse('core:tipo_investigaciones_costo_list')
