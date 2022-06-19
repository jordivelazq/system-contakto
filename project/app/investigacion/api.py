from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView
from rest_framework import mixins, viewsets

from .models import Investigacion
from .serializers import InvestigacionSerializer


class InvestigacionTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigaciones_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones'

        return context


class InvestigacionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer


    def get_queryset(self):
            qs = self.queryset.filter(cliente_solicitud__isnull = False,).order_by("cliente_solicitud")

            return qs


class InvestigacionUpdateView(UpdateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = Investigacion
    # form_class = UserEditForm
    fields = ['agente', 'contacto', 'fecha_recibido', 'hora_recibido']
    success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/investigacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionUpdateView, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.resultado = 0
        self.object.status = 0
        self.object.status_general = 0
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'La investigación ha sido actualizada')

        super(InvestigacionUpdateView, self).form_valid(form)

        return redirect(self.success_url)
