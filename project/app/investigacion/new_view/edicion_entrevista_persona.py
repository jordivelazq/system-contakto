from app.entrevista.forms import *
from app.entrevista.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets
from app.entrevista.services import EntrevistaService

from ..models import Investigacion
from django.shortcuts import HttpResponseRedirect

class EdicionEntrevistaPersonaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/edicion_enrtevista_personas/investigaciones_entrevista_detail.html'

    def post(self, request, *args, **kwargs):

        seccion_entrevista = self.kwargs['seccion_entrevista']
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        candidato = investigacion.candidato
        ep =  EntrevistaPersona.objects.get(investigacion=investigacion)
        
        #DATOS GENERALES
        if seccion_entrevista == 'datos-generales':
            telefonos = EntrevistaTelefono.objects.filter(persona_id=ep.pk)
            direccion = EntrevistaDireccion.objects.get(persona_id=ep.pk)
            origen = EntrevistaOrigen.objects.get(persona_id=ep.pk)
            licencia = EntrevistaLicencia.objects.get(persona_id=ep.pk)
            TelefonoFormSet = modelformset_factory(EntrevistaTelefono, extra=0, exclude=('persona', 'categoria',))

            candidato_form = EntrevistaPersonaForm(request.POST, instance=candidato) # A form bound to the POST data
            tel_formset = TelefonoFormSet(request.POST, prefix='telefonos')
            direccion_form = EntrevistaDireccionForm(request.POST, instance=direccion)
            origen_form = EntrevistaOrigenForm(request.POST, instance=origen, prefix='origen')
            licencia_form = EntrevistaLicenciaForm(request.POST, instance=licencia)

            if candidato_form.is_valid() and tel_formset.is_valid() and direccion_form.is_valid() and origen_form.is_valid() and licencia_form.is_valid():
                # candidato_form.save()
                tel_formset.save()
                direccion_form.save()
                origen_form.save()
                licencia_form.save()

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/datos-generales/'+str(investigacion.pk))
                # return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))
    
    def get_context_data(self, **kwargs):
        context = super(EdicionEntrevistaPersonaTemplateView, self).get_context_data(**kwargs)
        seccion_entrevista = self.kwargs['seccion_entrevista']
        
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        candidato = investigacion.candidato
        ep =  EntrevistaPersona.objects.get(investigacion=investigacion)
        
        context['investigacion'] = investigacion

        #DATOS GENERALES
        if seccion_entrevista == 'datos-generales':

            telefonos = EntrevistaTelefono.objects.filter(persona_id=ep.pk)
            direccion = EntrevistaDireccion.objects.get(persona_id=ep.pk)
            origen = EntrevistaOrigen.objects.get(persona_id=ep.pk)
            licencia = EntrevistaLicencia.objects.get(persona_id=ep.pk)
            # datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

            TelefonoFormSet = modelformset_factory(EntrevistaTelefono, extra=0, exclude=('persona', 'categoria',))

            context['seccion_entrevista'] = seccion_entrevista
            
            context['PrestacionViviendaFormSet'] = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

            context['candidato_form'] = EntrevistaPersonaForm(instance=candidato)
            context['tel_formset'] = TelefonoFormSet(queryset=telefonos, prefix='telefonos')
            context['direccion_form'] = EntrevistaDireccionForm(instance=direccion)
            context['origen_form'] = EntrevistaOrigenForm(instance=origen, prefix='origen')
            context['licencia_form'] = EntrevistaLicenciaForm(instance=licencia)

            return context
