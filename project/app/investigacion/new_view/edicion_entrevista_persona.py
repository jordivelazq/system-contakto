from app.adjuntos.models import Adjuntos
from app.entrevista.forms import *
from app.entrevista.models import *
from app.entrevista.services import EntrevistaService
from app.util.parallel import run_io_tasks_in_parallel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelformset_factory
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Investigacion
from app.investigacion.models import Investigacion, InvestigacionBitacora, GestorInvestigacion
from app.persona.models import Demanda


class EdicionEntrevistaPersonaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/edicion_enrtevista_personas/investigaciones_entrevista_detail.html'

    def post(self, request, *args, **kwargs):

        seccion_entrevista = self.kwargs['seccion_entrevista']
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        candidato = investigacion.candidato
        ep = EntrevistaPersona.objects.get(investigacion=investigacion)
        
        #DATOS GENERALES
        if seccion_entrevista == 'datos_generales':
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
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/datos_generales/'+str(investigacion.pk))
                # return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))
        
        #INFO PERSONAL
        if seccion_entrevista == 'info_personal':
            infopersonal = EntrevistaInfoPersonal.objects.get(persona_id=ep.pk)
            historial_empresa = EntrevistaHistorialEnEmpresa.objects.filter(persona_id=ep.pk)

            HistorialEmpresaFormset = modelformset_factory(EntrevistaHistorialEnEmpresa, extra=0, exclude=('persona', 'categoria',))

            infopersonal_form = EntrevistaInfoPersonalForm(request.POST, instance=infopersonal) # A form bound to the POST data
            historialempresa_formset = HistorialEmpresaFormset(request.POST, prefix='historial')
            
            if infopersonal_form.is_valid() and historialempresa_formset.is_valid():
                infopersonal_form.save()
                historialempresa_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/info_personal/'+str(investigacion.pk))

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))

                # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
        
        #SALUD, ACTIVIDADES Y HÁBITOS
        if seccion_entrevista == 'salud':
            salud = EntrevistaSalud.objects.get(persona_id=ep.pk)
            actividades = EntrevistaActividadesHabitos.objects.get(persona_id=ep.pk)
            candidato_form = EntrevistaSaludPersonaForm(request.POST, instance=candidato) # A form bound to the POST data
            salud_form = EntrevistaSaludForm(request.POST, instance=salud, prefix='salud')
            actividades_form = EntrevistaActividadesHabitosForm(request.POST, instance=actividades, prefix='actividades')
            
            if candidato_form.is_valid() and salud_form.is_valid() and actividades_form.is_valid():
                candidato_form.save()
                salud_form.save()
                actividades_form.save()

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))

                # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
                
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/salud/'+str(investigacion.pk))
        
        #INFORMACIÓN ACADÉMICA
        if seccion_entrevista == 'academica':
            academica = EntrevistaAcademica.objects.get(person_id=ep.pk)
            otro_idioma = EntrevistaOtroIdioma.objects.get(person_id=ep.pk)
            grados_escolares = EntrevistaGradoEscolaridad.objects.filter(person_id=ep.pk)

            GradoEscolaridadFormset = modelformset_factory(EntrevistaGradoEscolaridad, extra=0, exclude=('person', 'grado',))

        
            academica_form = EntrevistaAcademicaForm(request.POST, instance=academica)
            otro_idioma_form = EntrevistaOtroIdiomaForm(request.POST, instance=otro_idioma)
            gradosescolaridad_formset = GradoEscolaridadFormset(request.POST,  prefix='grados')

            if academica_form.is_valid() and otro_idioma_form.is_valid() and gradosescolaridad_formset.is_valid():
                academica_form.save()
                otro_idioma_form.save()
                gradosescolaridad_formset.save()

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))

                # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/academica/'+str(investigacion.pk))
    

        #SITUACIÓN VIVIENDA
        if seccion_entrevista == 'vivienda':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=2)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            situacion_vivienda = EntrevistaSituacionVivienda.objects.get(person_id=ep.pk)
            propietario_vivienda = EntrevistaPropietarioVivienda.objects.get(person_id=ep.pk)
            caracteristicas_vivienda = EntrevistaCaractaristicasVivienda.objects.get(person_id=ep.pk)
            tipo_inmueble_vivienda = EntrevistaTipoInmueble.objects.get(person_id=ep.pk)
            distribucion_vivienda = EntrevistaDistribucionDimensiones.objects.get(person_id=ep.pk)

        
            situacion_vivienda_form = EntrevistaSituacionViviendaForm(request.POST, instance=situacion_vivienda)
            propietario_vivienda_form = EntrevistaPropietarioViviendaForm(request.POST, instance=propietario_vivienda)
            caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(request.POST, instance=caracteristicas_vivienda)
            tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(request.POST, instance=tipo_inmueble_vivienda)
            distribucion_vivienda = EntrevistaDistribucionDimensionesForm(request.POST, instance=distribucion_vivienda)
            marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados', queryset=marco_familiar)

            if situacion_vivienda_form.is_valid() and propietario_vivienda_form.is_valid() and caracteristicas_vivienda_form.is_valid() and tipo_inmueble_vivienda_form.is_valid() and distribucion_vivienda.is_valid() and marcofamiliar_formset.is_valid():
                situacion_vivienda_form.save()
                propietario_vivienda_form.save()
                caracteristicas_vivienda_form.save()
                tipo_inmueble_vivienda_form.save()
                distribucion_vivienda.save()
                marcofamiliar_formset.save()

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))

                # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/vivienda/'+str(investigacion.pk))
        
        #MARCO FAMILIAR    
        if seccion_entrevista == 'familia':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=1)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados', queryset=marco_familiar)

            if marcofamiliar_formset.is_valid():
                marcofamiliar_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/familia/'+str(investigacion.pk))
        
        #INFORMACIÓN ECONÓMICA
        if seccion_entrevista == 'inf_economica':
            ingresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='ingreso')
            egresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='egreso')
            prestaciones_vivienda = EntrevistaPrestacionVivienda.objects.filter(persona_id=ep.pk)

            IngresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto'), form=MoneyFormatEntrevistaEconomicaForm)
            EgresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto',), form=MoneyFormatEntrevistaEconomicaForm)
            PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

            candidato = EntrevistaPersonaForm(request.POST, instance=candidato)
            ingresos_formset = IngresosFormset(request.POST, prefix='ingresos', queryset=ingresos)
            egresos_formset = EgresosFormset(request.POST, prefix='egresos', queryset=egresos)
            pv_formset = PrestacionViviendaFormSet(request.POST, prefix='prestaciones', queryset=prestaciones_vivienda)

            if ingresos_formset.is_valid() and egresos_formset.is_valid() and pv_formset.is_valid():
                run_io_tasks_in_parallel([
                    lambda: candidato.save(),
                    lambda: ingresos_formset.save(),
                    lambda: egresos_formset.save(),
                    lambda: pv_formset.save(),
                ])

                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/inf_economica/'+str(investigacion.pk))
        
        #BIENES
        if seccion_entrevista == 'bienes':
            tarjetas = EntrevistaTarjetaCreditoComercial.objects.filter(person_id=ep.pk)
            cuentas_deb = EntrevistaCuentaDebito.objects.filter(person_id=ep.pk)
            autos = EntrevistaAutomovil.objects.filter(person_id=ep.pk)
            bienesraices = EntrevistaBienesRaices.objects.filter(person_id=ep.pk)
            seguros = EntrevistaSeguro.objects.filter(person_id=ep.pk)
            deudas = EntrevistaDeudaActual.objects.filter(person_id=ep.pk)

            TarjetaCreditoComercialFormset = modelformset_factory(EntrevistaTarjetaCreditoComercial, extra=0, exclude=('person',), form=TarjetaCreditoComercialForm)
            CuentaDebitoFormset = modelformset_factory(EntrevistaCuentaDebito, extra=0, exclude=('person',), form=EntrevistaCuentaDebitoForm)
            AutomovilFormset = modelformset_factory(EntrevistaAutomovil, extra=0, exclude=('person',), form=EntrevistaAutomovilForm)
            BienesRaicesFormset = modelformset_factory(EntrevistaBienesRaices, extra=0, exclude=('person',), form=EntrevistaBienesRaicesForm)
            SeguroFormset = modelformset_factory(EntrevistaSeguro, extra=0, exclude=('person',))
            DeudaActualFormset = modelformset_factory(EntrevistaDeudaActual, extra=0, form=EntrevistaDeudaActualForm)

           
            tarjetas_formset = TarjetaCreditoComercialFormset(request.POST, prefix='tarjetas', queryset=tarjetas)
            cuentas_deb_formset = CuentaDebitoFormset(request.POST, prefix='cuentas_deb', queryset=cuentas_deb)
            autos_formset = AutomovilFormset(request.POST, prefix='autos', queryset=autos)
            bienesraices_formset = BienesRaicesFormset(request.POST, prefix='bienesraices', queryset=bienesraices)
            seguros_formset = SeguroFormset(request.POST, prefix='seguros', queryset=seguros)
            deudas_formset = DeudaActualFormset(request.POST, prefix='deudas', queryset=deudas)

            if tarjetas_formset.is_valid() and cuentas_deb_formset.is_valid() and autos_formset.is_valid() and bienesraices_formset.is_valid() and seguros_formset.is_valid() and deudas_formset.is_valid():
                tarjetas_formset.save()
                cuentas_deb_formset.save()
                autos_formset.save()
                bienesraices_formset.save()
                seguros_formset.save()
                deudas_formset.save()

                # Bitacora(action='bienes: ' + str(investigacion_id), user=request.user).save()

                # if 'redirect' in request.POST:
                #     return HttpResponseRedirect(request.POST.get('redirect'))

                # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/entrevista/editar/'+seccion_entrevista+'/exito') # Redirect after POST
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/bienes/'+str(investigacion.pk))

        #EVALUACIÓN
        if seccion_entrevista == 'evaluacion':
            # entrevista_investigacion = candidato.entrevistainvestigacion_set.all()[0]
            # entrevista_investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
            documentos = EntrevistaDocumentoCotejado.objects.filter(person_id=ep.pk)
            aspectos_hogar = EntrevistaAspectoHogar.objects.filter(person_id=ep.pk)
            aspectos_candidato = EntrevistaAspectoCandidato.objects.filter(person_id=ep.pk)

            DocumentoCotejadoFormset = modelformset_factory(EntrevistaDocumentoCotejado, extra=0, exclude=('person', 'tipo',), form=EntrevistaDocumentoCotejadoForm)
            AspectoHogarFormset = modelformset_factory(EntrevistaAspectoHogar, extra=0, exclude=('person', 'tipo',))
            AspectoCandidatoFormset = modelformset_factory(EntrevistaAspectoCandidato, extra=0, exclude=('person', 'tipo',))


            documentos_formset = DocumentoCotejadoFormset(request.POST, prefix='docs', queryset=documentos)
            aspectos_hogar_formset = AspectoHogarFormset(request.POST, prefix='asp_hogar', queryset=aspectos_hogar)
            aspectos_candidato_formset = AspectoCandidatoFormset(request.POST, prefix='asp_candidato', queryset=aspectos_candidato)
            investigacion_form = EntrevistaInvestigacionForm(request.POST, instance=entrevista_investigacion, prefix='investigacion')
            if documentos_formset.is_valid() and aspectos_hogar_formset.is_valid() and aspectos_candidato_formset.is_valid() and investigacion_form.is_valid():
                documentos_formset.save()
                aspectos_hogar_formset.save()
                aspectos_candidato_formset.save()
                investigacion_form.save()
                
                return HttpResponseRedirect('/investigaciones/investigaciones/entrevistal/detail/evaluacion/'+str(investigacion.pk))



    def get_context_data(self, **kwargs):
        context = super(EdicionEntrevistaPersonaTemplateView, self).get_context_data(**kwargs)
        seccion_entrevista = self.kwargs['seccion_entrevista']
        
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        candidato = investigacion.candidato

        adjuntos = Adjuntos.objects.filter(investigacion=investigacion)[0]
        context['adjuntos'] = adjuntos

        ep =  EntrevistaPersona.objects.get(investigacion=investigacion)
        
        context['investigacion'] = investigacion
        context['seccion_entrevista'] = seccion_entrevista
        context['bitacoras'] = InvestigacionBitacora.objects.filter(investigacion_id=self.kwargs['investigacion_id'], user=self.request.user).order_by('-datetime')


        #DATOS GENERALES
        if seccion_entrevista == 'datos_generales':

            telefonos = EntrevistaTelefono.objects.filter(persona_id=ep.pk)
            direccion = EntrevistaDireccion.objects.get(persona_id=ep.pk)
            origen = EntrevistaOrigen.objects.get(persona_id=ep.pk)
            licencia = EntrevistaLicencia.objects.get(persona_id=ep.pk)
            # datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

            TelefonoFormSet = modelformset_factory(EntrevistaTelefono, extra=0, exclude=('persona', 'categoria',))
            
            context['PrestacionViviendaFormSet'] = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

            context['candidato_form'] = EntrevistaPersonaForm(instance=candidato)
            context['tel_formset'] = TelefonoFormSet(queryset=telefonos, prefix='telefonos')
            context['direccion_form'] = EntrevistaDireccionForm(instance=direccion)
            context['origen_form'] = EntrevistaOrigenForm(instance=origen, prefix='origen')
            context['licencia_form'] = EntrevistaLicenciaForm(instance=licencia)

            

        #INFO PERSONAL
        if seccion_entrevista == 'info_personal':
            infopersonal = EntrevistaInfoPersonal.objects.get(persona_id=ep.pk)
            historial_empresa = EntrevistaHistorialEnEmpresa.objects.filter(persona_id=ep.pk)
            HistorialEmpresaFormset = modelformset_factory(EntrevistaHistorialEnEmpresa, extra=0, exclude=('persona', 'categoria',))

            infopersonal_form = EntrevistaInfoPersonalForm(instance=infopersonal)
            historialempresa_formset = HistorialEmpresaFormset(queryset=historial_empresa, prefix='historial')

            context['infopersonal_form'] = infopersonal_form
            context['historialempresa_formset'] = historialempresa_formset
        
        #SALUD, ACTIVIDADES Y HÁBITOS
        if seccion_entrevista == 'salud':
            salud = EntrevistaSalud.objects.get(persona_id=ep.pk)
            actividades = EntrevistaActividadesHabitos.objects.get(persona_id=ep.pk)

            candidato_form = EntrevistaSaludPersonaForm(instance=candidato)
            salud_form = EntrevistaSaludForm(instance=salud, prefix='salud')
            actividades_form = EntrevistaActividadesHabitosForm(instance=actividades, prefix='actividades')

            context['candidato_form'] = candidato_form
            context['salud_form'] = salud_form
            context['actividades_form'] = actividades_form

        
        #INFORMACIÓN ACADÉMICA
        if seccion_entrevista == 'academica':
            academica = EntrevistaAcademica.objects.get(person_id=ep.pk)
            otro_idioma = EntrevistaOtroIdioma.objects.get(person_id=ep.pk)
            grados_escolares = EntrevistaGradoEscolaridad.objects.filter(person_id=ep.pk)

            GradoEscolaridadFormset = modelformset_factory(EntrevistaGradoEscolaridad, extra=0, exclude=('person', 'grado',))

            academica_form = EntrevistaAcademicaForm(instance=academica)
            otro_idioma_form = EntrevistaOtroIdiomaForm(instance=otro_idioma)
            gradosescolaridad_formset = GradoEscolaridadFormset(queryset=grados_escolares, prefix='grados')

            context['academica_form'] = academica_form
            context['otro_idioma_form'] = otro_idioma_form
            context['gradosescolaridad_formset'] = gradosescolaridad_formset

        
        #SITUACIÓN VIVIENDA
        if seccion_entrevista == 'vivienda':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=2)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            situacion_vivienda = EntrevistaSituacionVivienda.objects.get(person_id=ep.pk)
            propietario_vivienda = EntrevistaPropietarioVivienda.objects.get(person_id=ep.pk)
            caracteristicas_vivienda = EntrevistaCaractaristicasVivienda.objects.get(person_id=ep.pk)
            tipo_inmueble_vivienda = EntrevistaTipoInmueble.objects.get(person_id=ep.pk)
            distribucion_vivienda = EntrevistaDistribucionDimensiones.objects.get(person_id=ep.pk)

           
            situacion_vivienda_form = EntrevistaSituacionViviendaForm(instance=situacion_vivienda)
            propietario_vivienda_form = EntrevistaPropietarioViviendaForm(instance=propietario_vivienda)
            caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(instance=caracteristicas_vivienda)
            tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(instance=tipo_inmueble_vivienda)
            distribucion_vivienda = EntrevistaDistribucionDimensionesForm(instance=distribucion_vivienda)
            marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')

            context['situacion_vivienda_form'] = situacion_vivienda_form
            context['propietario_vivienda_form'] = propietario_vivienda_form
            context['caracteristicas_vivienda_form'] = caracteristicas_vivienda_form
            context['tipo_inmueble_vivienda_form'] = tipo_inmueble_vivienda_form
            context['distribucion_vivienda'] = distribucion_vivienda
            context['marcofamiliar_formset'] = marcofamiliar_formset
        
        
        #MARCO FAMILIAR  
        if seccion_entrevista == 'familia':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=1)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')
          
            context['marcofamiliar_formset'] = marcofamiliar_formset
        

        #INFORMACIÓN ECONÓMICA
        if seccion_entrevista == 'inf_economica':
            ingresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='ingreso')
            egresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='egreso')
            prestaciones_vivienda = EntrevistaPrestacionVivienda.objects.filter(persona_id=ep.pk)

            IngresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto'), form=MoneyFormatEntrevistaEconomicaForm)
            EgresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto',), form=MoneyFormatEntrevistaEconomicaForm)
            PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)
  
            candidato_form = EntrevistaPersonaInfoEconomicaForm(instance=candidato)
            ingresos_formset = IngresosFormset(queryset=ingresos, prefix='ingresos')
            egresos_formset = EgresosFormset(queryset=egresos, prefix='egresos')
            pv_formset = PrestacionViviendaFormSet(queryset=prestaciones_vivienda, prefix='prestaciones')

            context['candidato_form'] = candidato_form
            context['ingresos_formset'] = ingresos_formset
            context['egresos_formset'] = egresos_formset
            context['pv_formset'] = pv_formset
        
        #BIENES
        if seccion_entrevista == 'bienes':
            tarjetas = EntrevistaTarjetaCreditoComercial.objects.filter(person_id=ep.pk)
            cuentas_deb = EntrevistaCuentaDebito.objects.filter(person_id=ep.pk)
            autos = EntrevistaAutomovil.objects.filter(person_id=ep.pk)
            bienesraices = EntrevistaBienesRaices.objects.filter(person_id=ep.pk)
            seguros = EntrevistaSeguro.objects.filter(person_id=ep.pk)
            deudas = EntrevistaDeudaActual.objects.filter(person_id=ep.pk)

            TarjetaCreditoComercialFormset = modelformset_factory(EntrevistaTarjetaCreditoComercial, extra=0, exclude=('person',), form=TarjetaCreditoComercialForm)
            CuentaDebitoFormset = modelformset_factory(EntrevistaCuentaDebito, extra=0, exclude=('person',), form=EntrevistaCuentaDebitoForm)
            AutomovilFormset = modelformset_factory(EntrevistaAutomovil, extra=0, exclude=('person',), form=EntrevistaAutomovilForm)
            BienesRaicesFormset = modelformset_factory(EntrevistaBienesRaices, extra=0, exclude=('person',), form=EntrevistaBienesRaicesForm)
            SeguroFormset = modelformset_factory(EntrevistaSeguro, extra=0, exclude=('person',))
            DeudaActualFormset = modelformset_factory(EntrevistaDeudaActual, extra=0, form=EntrevistaDeudaActualForm)

            tarjetas_formset = TarjetaCreditoComercialFormset(queryset=tarjetas, prefix='tarjetas')
            cuentas_deb_formset = CuentaDebitoFormset(queryset=cuentas_deb, prefix='cuentas_deb')
            autos_formset = AutomovilFormset(queryset=autos, prefix='autos')
            bienesraices_formset = BienesRaicesFormset(queryset=bienesraices, prefix='bienesraices')
            seguros_formset = SeguroFormset(queryset=seguros, prefix='seguros')
            deudas_formset = DeudaActualFormset(queryset=deudas, prefix='deudas')

            context['tarjetas_formset'] = tarjetas_formset
            context['cuentas_deb_formset'] = cuentas_deb_formset
            context['autos_formset'] = autos_formset
            context['bienesraices_formset'] = bienesraices_formset
            context['seguros_formset'] = seguros_formset
            context['deudas_formset'] = deudas_formset
       
        
        #EVALUACIÓN
        if seccion_entrevista == 'evaluacion':
            # entrevista_investigacion = candidato.entrevistainvestigacion_set.all()[0]
            entrevista_investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
            documentos = EntrevistaDocumentoCotejado.objects.filter(person_id=ep.pk)
            aspectos_hogar = EntrevistaAspectoHogar.objects.filter(person_id=ep.pk)
            aspectos_candidato = EntrevistaAspectoCandidato.objects.filter(person_id=ep.pk)

            DocumentoCotejadoFormset = modelformset_factory(EntrevistaDocumentoCotejado, extra=0, exclude=('person', 'tipo',), form=EntrevistaDocumentoCotejadoForm)
            AspectoHogarFormset = modelformset_factory(EntrevistaAspectoHogar, extra=0, exclude=('person', 'tipo',))
            AspectoCandidatoFormset = modelformset_factory(EntrevistaAspectoCandidato, extra=0, exclude=('person', 'tipo',))

           
            documentos_formset = DocumentoCotejadoFormset(queryset=documentos, prefix='docs')
            aspectos_hogar_formset = AspectoHogarFormset(queryset=aspectos_hogar, prefix='asp_hogar')
            aspectos_candidato_formset = AspectoCandidatoFormset(queryset=aspectos_candidato, prefix='asp_candidato')
            investigacion_form = EntrevistaInvestigacionForm(instance=entrevista_investigacion, prefix='investigacion')

            context['candidato_form'] = EntrevistaPersonaForm(instance=candidato)
            context['documentos_formset'] = documentos_formset
            context['aspectos_hogar_formset'] = aspectos_hogar_formset
            context['aspectos_candidato_formset'] = aspectos_candidato_formset
            context['investigacion_form'] = investigacion_form
		
        
        return context


class EdicionEntrevistaEjecutivoVisitaTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/ejecutivo_visitas/investigaciones_ejecutivo_visita_detail.html'

    def post(self, request, *args, **kwargs):

        seccion_entrevista = self.kwargs['seccion_entrevista']
        investigacion = Investigacion.objects.get(id=self.kwargs['pk'])
        candidato = investigacion.candidato
        ep = EntrevistaPersona.objects.get(investigacion=investigacion)
        
        #DATOS GENERALES
        if seccion_entrevista == 'datos_generales':
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

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/datos_generales/'+str(investigacion.pk))
               
        #INFO PERSONAL
        if seccion_entrevista == 'info_personal':
            infopersonal = EntrevistaInfoPersonal.objects.get(persona_id=ep.pk)
            historial_empresa = EntrevistaHistorialEnEmpresa.objects.filter(persona_id=ep.pk)

            HistorialEmpresaFormset = modelformset_factory(EntrevistaHistorialEnEmpresa, extra=0, exclude=('persona', 'categoria',))

            infopersonal_form = EntrevistaInfoPersonalForm(request.POST, instance=infopersonal) # A form bound to the POST data
            historialempresa_formset = HistorialEmpresaFormset(request.POST, prefix='historial')
            
            if infopersonal_form.is_valid() and historialempresa_formset.is_valid():
                infopersonal_form.save()
                historialempresa_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/info_personal/'+str(investigacion.pk))

        #SALUD, ACTIVIDADES Y HÁBITOS
        if seccion_entrevista == 'salud':
            salud = EntrevistaSalud.objects.get(persona_id=ep.pk)
            actividades = EntrevistaActividadesHabitos.objects.get(persona_id=ep.pk)
            candidato_form = EntrevistaSaludPersonaForm(request.POST, instance=candidato) # A form bound to the POST data
            salud_form = EntrevistaSaludForm(request.POST, instance=salud, prefix='salud')
            actividades_form = EntrevistaActividadesHabitosForm(request.POST, instance=actividades, prefix='actividades')
            
            if candidato_form.is_valid() and salud_form.is_valid() and actividades_form.is_valid():
                candidato_form.save()
                salud_form.save()
                actividades_form.save()
   
                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/salud/'+str(investigacion.pk))
        
        #INFORMACIÓN ACADÉMICA
        if seccion_entrevista == 'academica':
            academica = EntrevistaAcademica.objects.get(person_id=ep.pk)
            otro_idioma = EntrevistaOtroIdioma.objects.get(person_id=ep.pk)
            grados_escolares = EntrevistaGradoEscolaridad.objects.filter(person_id=ep.pk)

            GradoEscolaridadFormset = modelformset_factory(EntrevistaGradoEscolaridad, extra=0, exclude=('person', 'grado',))

        
            academica_form = EntrevistaAcademicaForm(request.POST, instance=academica)
            otro_idioma_form = EntrevistaOtroIdiomaForm(request.POST, instance=otro_idioma)
            gradosescolaridad_formset = GradoEscolaridadFormset(request.POST,  prefix='grados')

            if academica_form.is_valid() and otro_idioma_form.is_valid() and gradosescolaridad_formset.is_valid():
                academica_form.save()
                otro_idioma_form.save()
                gradosescolaridad_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/academica/'+str(investigacion.pk))
    

        #SITUACIÓN VIVIENDA
        if seccion_entrevista == 'vivienda':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=2)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            situacion_vivienda = EntrevistaSituacionVivienda.objects.get(person_id=ep.pk)
            propietario_vivienda = EntrevistaPropietarioVivienda.objects.get(person_id=ep.pk)
            caracteristicas_vivienda = EntrevistaCaractaristicasVivienda.objects.get(person_id=ep.pk)
            tipo_inmueble_vivienda = EntrevistaTipoInmueble.objects.get(person_id=ep.pk)
            distribucion_vivienda = EntrevistaDistribucionDimensiones.objects.get(person_id=ep.pk)

            situacion_vivienda_form = EntrevistaSituacionViviendaForm(request.POST, instance=situacion_vivienda)
            propietario_vivienda_form = EntrevistaPropietarioViviendaForm(request.POST, instance=propietario_vivienda)
            caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(request.POST, instance=caracteristicas_vivienda)
            tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(request.POST, instance=tipo_inmueble_vivienda)
            distribucion_vivienda = EntrevistaDistribucionDimensionesForm(request.POST, instance=distribucion_vivienda)
            marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados', queryset=marco_familiar)

            if situacion_vivienda_form.is_valid() and propietario_vivienda_form.is_valid() and caracteristicas_vivienda_form.is_valid() and tipo_inmueble_vivienda_form.is_valid() and distribucion_vivienda.is_valid() and marcofamiliar_formset.is_valid():
                situacion_vivienda_form.save()
                propietario_vivienda_form.save()
                caracteristicas_vivienda_form.save()
                tipo_inmueble_vivienda_form.save()
                distribucion_vivienda.save()
                marcofamiliar_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/vivienda/'+str(investigacion.pk))
        
        #MARCO FAMILIAR    
        if seccion_entrevista == 'familia':
            marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=1)
            MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

            marcofamiliar_formset = MarcoFamiliarFormset(request.POST, prefix='grados', queryset=marco_familiar)

            if marcofamiliar_formset.is_valid():
                marcofamiliar_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/familia/'+str(investigacion.pk))
        
        #INFORMACIÓN ECONÓMICA
        if seccion_entrevista == 'inf_economica':
            ingresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='ingreso')
            egresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='egreso')
            prestaciones_vivienda = EntrevistaPrestacionVivienda.objects.filter(persona_id=ep.pk)

            IngresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto'), form=MoneyFormatEntrevistaEconomicaForm)
            EgresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto',), form=MoneyFormatEntrevistaEconomicaForm)
            PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

            candidato.dependientes_economicos = request.POST.get('dependientes_economicos')
            ingresos_formset = IngresosFormset(request.POST, prefix='ingresos', queryset=ingresos)
            egresos_formset = EgresosFormset(request.POST, prefix='egresos', queryset=egresos)
            pv_formset = PrestacionViviendaFormSet(request.POST, prefix='prestaciones', queryset=prestaciones_vivienda)

            if ingresos_formset.is_valid() and egresos_formset.is_valid() and pv_formset.is_valid():
                run_io_tasks_in_parallel([
                    lambda: candidato.save(),
                    lambda: ingresos_formset.save(),
                    lambda: egresos_formset.save(),
                    lambda: pv_formset.save(),
                ])

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/inf_economica/'+str(investigacion.pk))
        
        #BIENES
        if seccion_entrevista == 'bienes':
            tarjetas = EntrevistaTarjetaCreditoComercial.objects.filter(person_id=ep.pk)
            cuentas_deb = EntrevistaCuentaDebito.objects.filter(person_id=ep.pk)
            autos = EntrevistaAutomovil.objects.filter(person_id=ep.pk)
            bienesraices = EntrevistaBienesRaices.objects.filter(person_id=ep.pk)
            seguros = EntrevistaSeguro.objects.filter(person_id=ep.pk)
            deudas = EntrevistaDeudaActual.objects.filter(person_id=ep.pk)

            TarjetaCreditoComercialFormset = modelformset_factory(EntrevistaTarjetaCreditoComercial, extra=0, exclude=('person',), form=TarjetaCreditoComercialForm)
            CuentaDebitoFormset = modelformset_factory(EntrevistaCuentaDebito, extra=0, exclude=('person',), form=EntrevistaCuentaDebitoForm)
            AutomovilFormset = modelformset_factory(EntrevistaAutomovil, extra=0, exclude=('person',), form=EntrevistaAutomovilForm)
            BienesRaicesFormset = modelformset_factory(EntrevistaBienesRaices, extra=0, exclude=('person',), form=EntrevistaBienesRaicesForm)
            SeguroFormset = modelformset_factory(EntrevistaSeguro, extra=0, exclude=('person',))
            DeudaActualFormset = modelformset_factory(EntrevistaDeudaActual, extra=0, form=EntrevistaDeudaActualForm)

           
            tarjetas_formset = TarjetaCreditoComercialFormset(request.POST, prefix='tarjetas', queryset=tarjetas)
            cuentas_deb_formset = CuentaDebitoFormset(request.POST, prefix='cuentas_deb', queryset=cuentas_deb)
            autos_formset = AutomovilFormset(request.POST, prefix='autos', queryset=autos)
            bienesraices_formset = BienesRaicesFormset(request.POST, prefix='bienesraices', queryset=bienesraices)
            seguros_formset = SeguroFormset(request.POST, prefix='seguros', queryset=seguros)
            deudas_formset = DeudaActualFormset(request.POST, prefix='deudas', queryset=deudas)

            if tarjetas_formset.is_valid() and cuentas_deb_formset.is_valid() and autos_formset.is_valid() and bienesraices_formset.is_valid() and seguros_formset.is_valid() and deudas_formset.is_valid():
                tarjetas_formset.save()
                cuentas_deb_formset.save()
                autos_formset.save()
                bienesraices_formset.save()
                seguros_formset.save()
                deudas_formset.save()

                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/bienes/'+str(investigacion.pk))
            
        #EVALUACIÓN
        if seccion_entrevista == 'evaluacion':
            # entrevista_investigacion = candidato.entrevistainvestigacion_set.all()[0]
            entrevista_investigacion = Investigacion.objects.get(id=self.kwargs['pk'])
            documentos = EntrevistaDocumentoCotejado.objects.filter(person_id=ep.pk)
            aspectos_hogar = EntrevistaAspectoHogar.objects.filter(person_id=ep.pk)
            aspectos_candidato = EntrevistaAspectoCandidato.objects.filter(person_id=ep.pk)

            DocumentoCotejadoFormset = modelformset_factory(EntrevistaDocumentoCotejado, extra=0, exclude=('person', 'tipo',), form=EntrevistaDocumentoCotejadoForm)
            AspectoHogarFormset = modelformset_factory(EntrevistaAspectoHogar, extra=0, exclude=('person', 'tipo',))
            AspectoCandidatoFormset = modelformset_factory(EntrevistaAspectoCandidato, extra=0, exclude=('person', 'tipo',))
            
            documentos_formset = DocumentoCotejadoFormset(request.POST, prefix='docs', queryset=documentos)
            aspectos_hogar_formset = AspectoHogarFormset(request.POST, prefix='asp_hogar', queryset=aspectos_hogar)
            aspectos_candidato_formset = AspectoCandidatoFormset(request.POST, prefix='asp_candidato', queryset=aspectos_candidato)
            investigacion_form = EntrevistaInvestigacionForm(request.POST, instance=entrevista_investigacion, prefix='investigacion')
            if documentos_formset.is_valid() and aspectos_hogar_formset.is_valid() and aspectos_candidato_formset.is_valid() and investigacion_form.is_valid():
                documentos_formset.save()
                aspectos_hogar_formset.save()
                aspectos_candidato_formset.save()
                investigacion_form.save()
                
                return HttpResponseRedirect('/investigaciones/investigaciones/ejecutivo-visitas/detail/evaluacion/'+str(investigacion.pk))

    def get_context_data(self, **kwargs):
        context = super(EdicionEntrevistaEjecutivoVisitaTemplateView, self).get_context_data(**kwargs)
        seccion_entrevista = self.kwargs['seccion_entrevista']
        
        investigacion = Investigacion.objects.get(id=self.kwargs['pk'])
        candidato = investigacion.candidato

        adjuntos = Adjuntos.objects.filter(investigacion=investigacion)[0]

        context['adjuntos'] = adjuntos

        entrevista = True
        try:
            ep =  EntrevistaPersona.objects.get(investigacion=investigacion)
        except EntrevistaPersona.DoesNotExist:
            entrevista = False

        context['entrevista'] = entrevista
        context['investigacion'] = investigacion
        context['seccion_entrevista'] = seccion_entrevista

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])

        context['title'] = 'Investigaciones / Coordinador de visitas domiciliarias / Detalles'

        context['bitacoras'] = InvestigacionBitacora.objects.filter(
            investigacion=inv, user_id=self.request.user.pk).order_by('-datetime')

        try:
            gInv = GestorInvestigacion.objects.get(
                investigacion=inv)
        except GestorInvestigacion.DoesNotExist:
            gInv = None

        context['gestor'] = gInv

        if entrevista:
            #DATOS GENERALES
            if seccion_entrevista == 'datos_generales':

                telefonos = EntrevistaTelefono.objects.filter(persona_id=ep.pk)
                direccion = EntrevistaDireccion.objects.get(persona_id=ep.pk)
                origen = EntrevistaOrigen.objects.get(persona_id=ep.pk)
                licencia = EntrevistaLicencia.objects.get(persona_id=ep.pk)
                # datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)

                TelefonoFormSet = modelformset_factory(EntrevistaTelefono, extra=0, exclude=('persona', 'categoria',))
                
                context['PrestacionViviendaFormSet'] = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)

                context['candidato_form'] = EntrevistaPersonaForm(instance=ep)
                context['tel_formset'] = TelefonoFormSet(queryset=telefonos, prefix='telefonos')
                context['direccion_form'] = EntrevistaDireccionForm(instance=direccion)
                context['origen_form'] = EntrevistaOrigenForm(instance=origen, prefix='origen')
                context['licencia_form'] = EntrevistaLicenciaForm(instance=licencia)

                

            #INFO PERSONAL
            if seccion_entrevista == 'info_personal':
                infopersonal = EntrevistaInfoPersonal.objects.get(persona_id=ep.pk)
                historial_empresa = EntrevistaHistorialEnEmpresa.objects.filter(persona_id=ep.pk)
                HistorialEmpresaFormset = modelformset_factory(EntrevistaHistorialEnEmpresa, extra=0, exclude=('persona', 'categoria',))

                infopersonal_form = EntrevistaInfoPersonalForm(instance=infopersonal)
                historialempresa_formset = HistorialEmpresaFormset(queryset=historial_empresa, prefix='historial')

                context['infopersonal_form'] = infopersonal_form
                context['historialempresa_formset'] = historialempresa_formset
            
            #SALUD, ACTIVIDADES Y HÁBITOS
            if seccion_entrevista == 'salud':
                salud, create = EntrevistaSalud.objects.get_or_create(persona_id=ep.pk)
                actividades = EntrevistaActividadesHabitos.objects.get(persona_id=ep.pk)

                candidato_form = EntrevistaSaludPersonaForm(instance=ep)
                salud_form = EntrevistaSaludForm(instance=salud, prefix='salud')
                actividades_form = EntrevistaActividadesHabitosForm(instance=actividades, prefix='actividades')

                context['candidato_form'] = candidato_form
                context['salud_form'] = salud_form
                context['actividades_form'] = actividades_form

                print('salud: ', salud, "vacio")
                print('actividades: ', actividades)

            
            #INFORMACIÓN ACADÉMICA
            if seccion_entrevista == 'academica':
                academica = EntrevistaAcademica.objects.get(person_id=ep.pk)
                otro_idioma = EntrevistaOtroIdioma.objects.get(person_id=ep.pk)
                grados_escolares = EntrevistaGradoEscolaridad.objects.filter(person_id=ep.pk)

                GradoEscolaridadFormset = modelformset_factory(EntrevistaGradoEscolaridad, extra=0, exclude=('person', 'grado',))

                academica_form = EntrevistaAcademicaForm(instance=academica)
                otro_idioma_form = EntrevistaOtroIdiomaForm(instance=otro_idioma)
                gradosescolaridad_formset = GradoEscolaridadFormset(queryset=grados_escolares, prefix='grados')

                context['academica_form'] = academica_form
                context['otro_idioma_form'] = otro_idioma_form
                context['gradosescolaridad_formset'] = gradosescolaridad_formset

            
            #SITUACIÓN VIVIENDA
            if seccion_entrevista == 'vivienda':
                marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=2)
                MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

                situacion_vivienda = EntrevistaSituacionVivienda.objects.get(person_id=ep.pk)
                propietario_vivienda = EntrevistaPropietarioVivienda.objects.get(person_id=ep.pk)
                caracteristicas_vivienda = EntrevistaCaractaristicasVivienda.objects.get(person_id=ep.pk)
                tipo_inmueble_vivienda = EntrevistaTipoInmueble.objects.get(person_id=ep.pk)
                distribucion_vivienda = EntrevistaDistribucionDimensiones.objects.get(person_id=ep.pk)

            
                situacion_vivienda_form = EntrevistaSituacionViviendaForm(instance=situacion_vivienda)
                propietario_vivienda_form = EntrevistaPropietarioViviendaForm(instance=propietario_vivienda)
                caracteristicas_vivienda_form = EntrevistaCaractaristicasViviendaForm(instance=caracteristicas_vivienda)
                tipo_inmueble_vivienda_form = EntrevistaTipoInmuebleForm(instance=tipo_inmueble_vivienda)
                distribucion_vivienda = EntrevistaDistribucionDimensionesForm(instance=distribucion_vivienda)
                marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')

                context['situacion_vivienda_form'] = situacion_vivienda_form
                context['propietario_vivienda_form'] = propietario_vivienda_form
                context['caracteristicas_vivienda_form'] = caracteristicas_vivienda_form
                context['tipo_inmueble_vivienda_form'] = tipo_inmueble_vivienda_form
                context['distribucion_vivienda'] = distribucion_vivienda
                context['marcofamiliar_formset'] = marcofamiliar_formset
            
            
            #MARCO FAMILIAR  
            if seccion_entrevista == 'familia':
                marco_familiar = EntrevistaMiembroMarcoFamiliar.objects.filter(person_id=ep.pk, category=1)
                MarcoFamiliarFormset = modelformset_factory(EntrevistaMiembroMarcoFamiliar, extra=0, exclude=('person', 'tipo', 'category'))

                marcofamiliar_formset = MarcoFamiliarFormset(queryset=marco_familiar, prefix='grados')
            
                context['marcofamiliar_formset'] = marcofamiliar_formset
            

            #INFORMACIÓN ECONÓMICA
            if seccion_entrevista == 'inf_economica':
                ingresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='ingreso')
                egresos = EntrevistaEconomica.objects.filter(person_id=ep.pk, tipo='egreso')
                prestaciones_vivienda = EntrevistaPrestacionVivienda.objects.filter(persona_id=ep.pk)

                IngresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto'), form=MoneyFormatEntrevistaEconomicaForm)
                EgresosFormset = modelformset_factory(EntrevistaEconomica, extra=0, exclude=('person', 'tipo', 'concepto',), form=MoneyFormatEntrevistaEconomicaForm)
                PrestacionViviendaFormSet = modelformset_factory(EntrevistaPrestacionVivienda, extra=0, exclude=('persona', 'categoria_viv'), formfield_callback=EntrevistaService.datefields_callback)
    
                candidato_form = EntrevistaPersonaInfoEconomicaForm(instance=candidato)
                ingresos_formset = IngresosFormset(queryset=ingresos, prefix='ingresos')
                egresos_formset = EgresosFormset(queryset=egresos, prefix='egresos')
                pv_formset = PrestacionViviendaFormSet(queryset=prestaciones_vivienda, prefix='prestaciones')

                context['candidato_form'] = candidato_form
                context['ingresos_formset'] = ingresos_formset
                context['egresos_formset'] = egresos_formset
                context['pv_formset'] = pv_formset
            
            #BIENES
            if seccion_entrevista == 'bienes':
                tarjetas = EntrevistaTarjetaCreditoComercial.objects.filter(person_id=ep.pk)
                cuentas_deb = EntrevistaCuentaDebito.objects.filter(person_id=ep.pk)
                autos = EntrevistaAutomovil.objects.filter(person_id=ep.pk)
                bienesraices = EntrevistaBienesRaices.objects.filter(person_id=ep.pk)
                seguros = EntrevistaSeguro.objects.filter(person_id=ep.pk)
                deudas = EntrevistaDeudaActual.objects.filter(person_id=ep.pk)

                TarjetaCreditoComercialFormset = modelformset_factory(EntrevistaTarjetaCreditoComercial, extra=0, exclude=('person',), form=TarjetaCreditoComercialForm)
                CuentaDebitoFormset = modelformset_factory(EntrevistaCuentaDebito, extra=0, exclude=('person',), form=EntrevistaCuentaDebitoForm)
                AutomovilFormset = modelformset_factory(EntrevistaAutomovil, extra=0, exclude=('person',), form=EntrevistaAutomovilForm)
                BienesRaicesFormset = modelformset_factory(EntrevistaBienesRaices, extra=0, exclude=('person',), form=EntrevistaBienesRaicesForm)
                SeguroFormset = modelformset_factory(EntrevistaSeguro, extra=0, exclude=('person',))
                DeudaActualFormset = modelformset_factory(EntrevistaDeudaActual, extra=0, form=EntrevistaDeudaActualForm)

                tarjetas_formset = TarjetaCreditoComercialFormset(queryset=tarjetas, prefix='tarjetas')
                cuentas_deb_formset = CuentaDebitoFormset(queryset=cuentas_deb, prefix='cuentas_deb')
                autos_formset = AutomovilFormset(queryset=autos, prefix='autos')
                bienesraices_formset = BienesRaicesFormset(queryset=bienesraices, prefix='bienesraices')
                seguros_formset = SeguroFormset(queryset=seguros, prefix='seguros')
                deudas_formset = DeudaActualFormset(queryset=deudas, prefix='deudas')

                context['tarjetas_formset'] = tarjetas_formset
                context['cuentas_deb_formset'] = cuentas_deb_formset
                context['autos_formset'] = autos_formset
                context['bienesraices_formset'] = bienesraices_formset
                context['seguros_formset'] = seguros_formset
                context['deudas_formset'] = deudas_formset
        
            
            #EVALUACIÓN
            if seccion_entrevista == 'evaluacion':
                # entrevista_investigacion = candidato.entrevistainvestigacion_set.all()[0]
                entrevista_investigacion = Investigacion.objects.get(id=self.kwargs['pk'])
                documentos = EntrevistaDocumentoCotejado.objects.filter(person_id=ep.pk)
                aspectos_hogar = EntrevistaAspectoHogar.objects.filter(person_id=ep.pk)
                aspectos_candidato = EntrevistaAspectoCandidato.objects.filter(person_id=ep.pk)

                DocumentoCotejadoFormset = modelformset_factory(EntrevistaDocumentoCotejado, extra=0, exclude=('person', 'tipo',), form=EntrevistaDocumentoCotejadoForm)
                AspectoHogarFormset = modelformset_factory(EntrevistaAspectoHogar, extra=0, exclude=('person', 'tipo',))
                AspectoCandidatoFormset = modelformset_factory(EntrevistaAspectoCandidato, extra=0, exclude=('person', 'tipo',))

            
                documentos_formset = DocumentoCotejadoFormset(queryset=documentos, prefix='docs')
                aspectos_hogar_formset = AspectoHogarFormset(queryset=aspectos_hogar, prefix='asp_hogar')
                aspectos_candidato_formset = AspectoCandidatoFormset(queryset=aspectos_candidato, prefix='asp_candidato')
                investigacion_form = EntrevistaInvestigacionForm(instance=entrevista_investigacion, prefix='investigacion')

                context['candidato_form'] = EntrevistaPersonaForm(instance=ep)
                context['documentos_formset'] = documentos_formset
                context['aspectos_hogar_formset'] = aspectos_hogar_formset
                context['aspectos_candidato_formset'] = aspectos_candidato_formset
                context['investigacion_form'] = investigacion_form
		
        return context
