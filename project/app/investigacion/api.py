from app.compania.forms import *
from app.investigacion.forms import *
from app.persona.form_functions import *
from app.persona.forms import *
from app.entrevista.services import *
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)
from rest_framework import mixins, viewsets

from .models import GestorInvestigacion, Investigacion, InvestigacionBitacora
from .serializers import InvestigacionSerializer
from app.persona.models import *


class InvestigacionTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigaciones_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionTemplateView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Investigaciones'

        return context


class InvestigacionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Investigacion.objects.all()
    serializer_class = InvestigacionSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            cliente_solicitud__isnull=False,).order_by("cliente_solicitud")

        return qs


class InvestigacionDetailView(DetailView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = Investigacion
    context_object_name = 'investigacion'
    template_name = 'investigaciones/investigacion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionDetailView,
                        self).get_context_data(**kwargs)

        inv = Investigacion.objects.get(pk=self.kwargs['pk'])
        context['bitacoras'] = InvestigacionBitacora.objects.filter(investigacion_id=self.kwargs['pk'])

        context['tajectorias_laborales'] = TrayectoriaLaboral.objects.filter(persona=inv.candidato)

        try:
            gInv = GestorInvestigacion.objects.get(
                investigacion_id=self.kwargs['pk'])
        except GestorInvestigacion.DoesNotExist:
            gInv = None

        context['gestor'] = gInv

        return context


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
        context = super(InvestigacionUpdateView,
                        self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.resultado = 0
        self.object.status = 0
        self.object.status_general = 0
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS,
                             'La investigación ha sido actualizada')

        super(InvestigacionUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class GestorInvestigacionCreateView(CreateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = GestorInvestigacion
    fields = ['gestor', 'fecha_asignacion']
    # success_url = reverse_lazy('investigaciones:investigaciones_list')
    template_name = 'investigaciones/gestores/gestor_form.html'

    def get_context_data(self, **kwargs):
        context = super(GestorInvestigacionCreateView,
                        self).get_context_data(**kwargs)

        context['investigacion_id'] = self.kwargs['investigacion_id']

        return context

    def form_valid(self, form):

        inv = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        self.object = form.save(commit=False)
        self.object.investigacion = inv
        self.object.save()

        inv.agente_id = self.object.gestor.usuario.pk

        bitacora = InvestigacionBitacora()
        bitacora.user_id = self.request.user.pk
        bitacora.investigacion = inv
        bitacora.servicio = "Gestor"
        bitacora.observaciones = "Asignación de gestor"
        bitacora.save()

        return super(GestorInvestigacionCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El gestor ha sido asignado')
        return reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['pk']})


class CandidatoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/investigacion_candidato_edit.html'

    def post(self, request, *args, **kwargs):

        investigacion = Investigacion.objects.select_related(
            'compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        formCandidato = CandidatoAltaForm(
            request.POST, prefix='candidato', instance=investigacion.candidato)

        if formCandidato.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 'El candidato ha sido guardado')
            formCandidato.save()
            # return redirect(reverse('investigaciones:investigacion_detail', kwargs={ "pk": self.kwargs['investigacion_id']}))
        else:
            msg_param = ''
        ####################### Origen #######################
        formOrigen = OrigenAltaForma(request.POST, prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(
            request.POST, prefix='origen')
        if has_info(request.POST, prefix='origen', investigacion=investigacion):
            if formOrigen.is_valid():
                origen = formOrigen.save(commit=False)
                origen.persona = investigacion.candidato
                origen.save()
            else:
                msg_param = ''
        ####################### Dirección #######################
        formDireccion = DireccionForm(request.POST, prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(
            request.POST, prefix='direccion')
        if has_info(request.POST, prefix='direccion', investigacion=investigacion):
            if formDireccion.is_valid():
                direccion = formDireccion.save(commit=False)
                direccion.persona = investigacion.candidato
                direccion.save()
            else:
                msg_param = ''
        ####################### Teléfono1 (casa)  #######################
        formTelefono1 = TelefonoForm(request.POST, prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(
            request.POST, prefix='telefono1')
        if has_info(request.POST, prefix='telefono1', investigacion=investigacion):
            if formTelefono1.is_valid():
                tel1 = formTelefono1.save(commit=False)
                tel1.persona = investigacion.candidato
                tel1.categoria = 'casa'
                tel1.save()
            else:
                msg_param = ''
        ####################### Teléfono2 (movil)  #######################
        formTelefono2 = TelefonoForm(request.POST, prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(
            request.POST, prefix='telefono2')
        if has_info(request.POST, prefix='telefono2', investigacion=investigacion):
            if formTelefono2.is_valid():
                tel2 = formTelefono2.save(commit=False)
                tel2.persona = investigacion.candidato
                tel2.categoria = 'movil'
                tel2.save()
            else:
                msg_param = ''
        ####################### Teléfono3 (recado)  #######################
        formTelefono3 = TelefonoForm(request.POST, prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(
            request.POST, prefix='telefono3')
        if has_info(request.POST, prefix='telefono3', investigacion=investigacion):
            if formTelefono3.is_valid():
                tel3 = formTelefono3.save(commit=False)
                tel3.persona = investigacion.candidato
                tel3.categoria = 'recado'
                tel3.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Infonavit #######################
        formPrestacionViviendaInfonavit = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_infonavit')
        if has_info(request.POST, prefix='prestacion_vivienda_infonavit', investigacion=investigacion):
            if formPrestacionViviendaInfonavit.is_valid():
                prestacionViviendaInfonavit = formPrestacionViviendaInfonavit.save(
                    commit=False)
                prestacionViviendaInfonavit.persona = investigacion.candidato
                prestacionViviendaInfonavit.categoria_viv = 'infonavit'
                prestacionViviendaInfonavit.save()
            else:
                msg_param = ''
        ####################### PrestacionVivienda Fonacot #######################
        formPrestacionViviendaFonacot = PrestacionViviendaForma(
            request.POST, prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(request.POST, prefix='prestacion_vivienda_fonacot')
        if has_info(request.POST, prefix='prestacion_vivienda_fonacot', investigacion=investigacion):
            if formPrestacionViviendaFonacot.is_valid():
                prestacionViviendaFonacot = formPrestacionViviendaFonacot.save(
                    commit=False)
                prestacionViviendaFonacot.persona = investigacion.candidato
                prestacionViviendaFonacot.categoria_viv = 'fonacot'
                prestacionViviendaFonacot.save()
            else:
                msg_param = ''
        ####################### Legalidad #######################
        formLegalidad = LegalidadAltaForma(
            request.POST, prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(request.POST, prefix='legalidad')
        if has_info(request.POST, prefix='legalidad', investigacion=investigacion):
            if formLegalidad.is_valid():
                legalidad = formLegalidad.save(commit=False)
                legalidad.persona = investigacion.candidato
                legalidad.save()
            else:
                msg_param = ''

        return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id']}))

        '''
        ####################### Demanda
        formDemanda = DemandaFormSet(request.POST)

        ####################### Seguro #######################
        formSeguro = SeguroAltaForma(request.POST, prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(request.POST, prefix='seguro')
        if has_info(request.POST, prefix='seguro', investigacion=investigacion):
            if formSeguro.is_valid():
                seguro = formSeguro.save(commit=False)
                seguro.persona = investigacion.candidato
                seguro.save()
            else:
                msg_param = ''

        ####################### Investigación #######################

        formSucursal = CompaniaSucursalForm(request.POST.get('investigacion-compania'), request.POST.get('investigacion-sucursal'), prefix='investigacion')

        formInvestigacion = InvestigacionEditarForm(request.POST, prefix='investigacion', instance=investigacion, agt_id=agente_id)
        if request.POST.get('investigacion-sucursal', '') == '':
            msg.append('Es necesario seleccionar sucursal')
            status = 'danger'
        elif not formInvestigacion.is_valid():
            msg_param = ''
        else:
            ####################### Demanda
            if formDemanda.is_valid():
                for formItem in formDemanda:
                    demanda = formItem.save(commit=False)
                    demanda.persona = investigacion.candidato
                    demanda.save()
            else:
                msg_param = formDemanda.errors

            investigacion = formInvestigacion.save()
            investigacion.status_active = True

            investigacion.save()

            if Cobranza.objects.filter(investigacion=investigacion).count() == 0:
                Cobranza(investigacion=investigacion).save()

            if msg_param != '':
                if 'guardar_sucursal' in request.POST:
                    return HttpResponseRedirect('/empresa/' + str(investigacion.compania.id) + '/sucursales?investigacion=' + str(investigacion.id))
                if 'redirect' in request.POST:
                    return HttpResponseRedirect(request.POST.get('redirect'))
                return HttpResponseRedirect('/candidato/investigacion/'+str(investigacion_id)+'/editar'+msg_param)
        '''

    def get_context_data(self, **kwargs):
        context = super(CandidatoTemplateView, self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.select_related(
            'compania', 'candidato').get(id=self.kwargs['investigacion_id'])

        agente_id = investigacion.agente.id
        origen = investigacion.candidato.origen_set.all()
        direccion = investigacion.candidato.direccion_set.all()
        tel1 = investigacion.candidato.telefono_set.filter(categoria='casa')
        tel2 = investigacion.candidato.telefono_set.filter(categoria='movil')
        tel3 = investigacion.candidato.telefono_set.filter(categoria='recado')
        infonavit = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='infonavit')
        fonacot = investigacion.candidato.prestacionvivienda_set.filter(
            categoria_viv='fonacot')
        legalidad = investigacion.candidato.legalidad_set.all()
        demanda = investigacion.candidato.demanda_set.all()
        seguro = investigacion.candidato.seguro_set.all()

        context['investigacion'] = investigacion

        context['formCandidato'] = CandidatoAltaForm(
            prefix='candidato', instance=investigacion.candidato)
        context['formInvestigacion'] = InvestigacionEditarForm(prefix='investigacion', instance=investigacion, initial={
                                                               'compania': investigacion.compania.id}, agt_id=agente_id)
        context['formOrigen'] = OrigenAltaForma(
            prefix='origen', instance=origen[0]) if origen else OrigenAltaForma(prefix='origen')
        context['formDireccion'] = DireccionForm(
            prefix='direccion', instance=direccion[0]) if direccion else DireccionForm(prefix='direccion')
        context['formTelefono1'] = TelefonoForm(
            prefix='telefono1', instance=tel1[0]) if tel1 else TelefonoForm(prefix='telefono1')
        context['formTelefono2'] = TelefonoForm(
            prefix='telefono2', instance=tel2[0]) if tel2 else TelefonoForm(prefix='telefono2')
        context['formTelefono3'] = TelefonoForm(
            prefix='telefono3', instance=tel3[0]) if tel3 else TelefonoForm(prefix='telefono3')
        context['formPrestacionViviendaInfonavit'] = PrestacionViviendaForma(
            prefix='prestacion_vivienda_infonavit', instance=infonavit[0]) if infonavit else PrestacionViviendaForma(prefix='prestacion_vivienda_infonavit')
        context['formPrestacionViviendaFonacot'] = PrestacionViviendaForma(
            prefix='prestacion_vivienda_fonacot', instance=fonacot[0]) if fonacot else PrestacionViviendaForma(prefix='prestacion_vivienda_fonacot')
        context['formLegalidad'] = LegalidadAltaForma(
            prefix='legalidad', instance=legalidad[0]) if legalidad else LegalidadAltaForma(prefix='legalidad')
        # formDemanda = DemandaFormSet(queryset=Demanda.objects.filter(persona=investigacion.candidato))
        context['formSeguro'] = SeguroAltaForma(
            prefix='seguro', instance=seguro[0]) if seguro else SeguroAltaForma(prefix='seguro')
        context['formSucursal'] = CompaniaSucursalForm(
            investigacion.compania.id, investigacion.sucursal.id if investigacion.sucursal else None, prefix='investigacion')

        return context


class ClienteSolicitudCreateTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Client",]
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):
        # cliente = Cliente.objects.get(user=request.user)
        u = User.objects.get(id=self.request.user.pk)
        cliente = ClienteUser.objects.get(username=u.username)
        solicitud = ClienteSolicitud()
        solicitud.cliente = cliente
        solicitud.save()
        return redirect('clientes:clientes_solicitud_detail', pk=solicitud.pk, **kwargs)


class ClienteSolicitudDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = [u"Client", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitud
    context_object_name = "cliente_solicitud"
    template_name = 'clientes/solicitudes/solicitud_detail.html'

    page = {
        'title': 'Detalle de Solicitud',
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudDetailView, self).get_context_data(**kwargs)

        context['page'] = self.page
        context['cliente_solicitud_candidatos'] = ClienteSolicitudCandidato.objects.filter(cliente_solicitud_id=self.object.pk)
        

        return context


class PersonaTrayectoriaCrearTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Client",]
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):

        # Tomar investigacion
        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        nva_trayectoria = TrayectoriaLaboral()
        nva_trayectoria.persona = investigacion.candidato
        nva_trayectoria.compania = investigacion.compania
        nva_trayectoria.save()

        Evaluacion(trayectoriaLaboral=nva_trayectoria).save()
       
        messages.add_message(self.request, messages.SUCCESS, 'El solicitud ha sido enviada satisfactoriamente.')
        return redirect(reverse('investigaciones:investigacion_persona_trayectoria_laboral_edit', 
            kwargs={"investigacion_id": self.kwargs['investigacion_id'],"pk": nva_trayectoria.pk, }))
        


class PersonaTrayectoriaEditTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'investigaciones/personas/trayectoria_laboral_form.html'

    # def post(self, request, *args, **kwargs):

    #     investigacion = Investigacion.objects.select_related(
    #         'compania', 'candidato').get(id=self.kwargs['investigacion_id'])


    #     return redirect(reverse('investigaciones:investigacion_detail', kwargs={"pk": self.kwargs['investigacion_id'], }))

    def post(self, request, *args, **kwargs):
        
        exito = True

        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])
        trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(pk=self.kwargs['pk'])
        evaluacion = trayectoria_empresa.evaluacion_set.all()
        opinion_jefe = trayectoria_empresa.opinion_set.filter(categoria=1) if evaluacion else None 
        opinion_rh = trayectoria_empresa.opinion_set.filter(categoria=2) if evaluacion else None
        carta_laboral = trayectoria_empresa.cartalaboral if hasattr(trayectoria_empresa, 'cartalaboral') else None
        datos_generales = trayectoria_empresa.datosgenerales if hasattr(trayectoria_empresa, 'datosgenerales') else None

        informantes = evaluacion[0].informante_set.all() if evaluacion else None
        informante1 = informantes[0] if informantes else None
        informante2 = (informantes[1] if informantes.count() > 1 else None) if informantes else None

        formTrayectoria = TrayectoriaForm(request.POST, prefix='trayectoria', instance=trayectoria_empresa)

        if formTrayectoria.is_valid(): 
            trayectoria_empresa = formTrayectoria.save()
        else:
            # logger.info('formTrayectoria invalid')
            print("####### 01 #######")
            exito = False


        ############## Carta Laboral
        formCartaLaboral = CartaLaboralForma(request.POST, instance=carta_laboral)
        if formCartaLaboral.is_valid():
            carta_laboral = formCartaLaboral.save(commit=False)
            carta_laboral.trayectoriaLaboral = trayectoria_empresa
            carta_laboral.save()
        else:
            # logger.info('formCartaLaboral invalid')
            print("####### 02 #######")
            exito = False
        
        ############## Datos Generales
        formDatosGenerales = DatosGeneralesForma(request.POST, instance=datos_generales)
        if formDatosGenerales.is_valid():
            datos_generales = formDatosGenerales.save(commit=False)
            datos_generales.trayectoriaLaboral = trayectoria_empresa
            datos_generales.save()
        else:
            # logger.info('formDatosGenerales invalid')
            print("####### 03 #######")
            exito = False

        ############## Evaluación ##############
        formEvaluacion = EvaluacionForm(request.POST, prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(request.POST, prefix='evaluacion')
        if has_info_trayectoria(request.POST, prefix='evaluacion', trayectoria=trayectoria_empresa):
            if formEvaluacion.is_valid():
                evaluacion = formEvaluacion.save(commit=False)
                evaluacion.trayectoriaLaboral = trayectoria_empresa
                evaluacion.save()
            else:
                print("####### 05 #######")
                # logger.info('formEvaluacion invalid')
                exito = False

        ############## Opinion (Jefe) ##############
        formOpinionJefe = OpinionAltaForma(request.POST, prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(request.POST, prefix='opinion_jefe')
        if has_info_trayectoria(request.POST, prefix='opinion_jefe', trayectoria=trayectoria_empresa):
            if formOpinionJefe.is_valid():
                opinion_jefe = formOpinionJefe.save(commit=False)
                opinion_jefe.trayectoriaLaboral = trayectoria_empresa
                opinion_jefe.categoria = 1
                opinion_jefe.save()
            else:
                print("####### 05 #######")
                # logger.info('opinion_jefe invalid')
                exito = False

        ############## Opinion (RH) ##############
        formOpinionRH = OpinionAltaForma(request.POST, prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(request.POST, prefix='opinion_rh')
        if has_info_trayectoria(request.POST, prefix='opinion_rh', trayectoria=trayectoria_empresa):
            if formOpinionRH.is_valid():
                opinion_rh = formOpinionRH.save(commit=False)
                opinion_rh.trayectoriaLaboral = trayectoria_empresa
                opinion_rh.categoria = 2
                try:
                    opinion_rh.save()
                except Exception as error:
                    # logger.info('opinion_rh error')
                    # msg.append({
                    #     "text": "Opinion RH: " + str(error),
                    #     "status": "danger"
                    # })
                    print("####### 06 #######")
                    exito = False	
            else:
                pass
                # logger.info('formOpinionRH invalid')
                exito = False

        ############## Informantes  ##############
        formInformante1 = InformanteAltaForma(request.POST, prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(request.POST, prefix='informante1')
        if has_info_trayectoria(request.POST, prefix='informante1', trayectoria=trayectoria_empresa):
            informante1 = formInformante1.save(commit=False)
            informante1.evaluacion = evaluacion
            informante1.save()

        formInformante2 = InformanteAltaForma(request.POST, prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(request.POST, prefix='informante2')
        if has_info_trayectoria(request.POST, prefix='informante2', trayectoria=trayectoria_empresa):
            informante2 = formInformante2.save(commit=False)
            informante2.evaluacion = evaluacion
            informante2.save()

        # b = Bitacora(action='trayectoria-editar: ' + str(trayectoria_empresa), user=request.user)
        # b.save()
        if exito:
            return redirect(reverse('investigaciones:investigacion_detail', kwargs={"investigacion_id": self.kwargs['investigacion_id'], }))
            # if 'guardar_sucursal' in request.POST:
            #     return HttpResponseRedirect('/empresa/' + str(trayectoria_empresa.compania.id) + '/sucursal/nueva?investigacion_id=' + investigacion_id + '&trayectoria=' + trayectoria_id)
            
            # if 'redirect' in request.POST:
            #     return HttpResponseRedirect(request.POST.get('redirect'))

            # return HttpResponseRedirect('/candidato/investigacion/'+investigacion_id+'/editar/trayectoria/'+trayectoria_id+'/exito')
       

    def get_context_data(self, **kwargs):
        context = super(PersonaTrayectoriaEditTemplateView, self).get_context_data(**kwargs)

        investigacion = Investigacion.objects.get(id=self.kwargs['investigacion_id'])

        trayectoria_empresa = investigacion.candidato.trayectorialaboral_set.get(pk=self.kwargs['pk'])
        evaluacion = trayectoria_empresa.evaluacion_set.all()
        opinion_jefe = trayectoria_empresa.opinion_set.filter(categoria=1) if evaluacion else None 
        opinion_rh = trayectoria_empresa.opinion_set.filter(categoria=2) if evaluacion else None
        carta_laboral = trayectoria_empresa.cartalaboral if hasattr(trayectoria_empresa, 'cartalaboral') else None
        datos_generales = trayectoria_empresa.datosgenerales if hasattr(trayectoria_empresa, 'datosgenerales') else None

        informantes = evaluacion[0].informante_set.all() if evaluacion else None
        informante1 = informantes[0] if informantes else None
        informante2 = (informantes[1] if informantes.count() > 1 else None) if informantes else None
        
        datos_entrevista = EntrevistaService.getDatosEntrevista(investigacion)
        formSucursal = CompaniaSucursalForm(trayectoria_empresa.compania.id, trayectoria_empresa.sucursal.id if trayectoria_empresa.sucursal else None, prefix='trayectoria')

        formTrayectoria = TrayectoriaForm(prefix='trayectoria', instance=trayectoria_empresa)
        formCartaLaboral = CartaLaboralForma(instance=carta_laboral) if carta_laboral else CartaLaboralForma()
        formDatosGenerales = DatosGeneralesForma(instance=datos_generales) if datos_generales else DatosGeneralesForma()
        formEvaluacion = EvaluacionForm(prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')
        
        #formEvaluacion = EvaluacionForm(prefix='evaluacion', instance=evaluacion[0]) if evaluacion else EvaluacionForm(prefix='evaluacion')
        formOpinionJefe = OpinionAltaForma(prefix='opinion_jefe', instance=opinion_jefe[0]) if opinion_jefe else OpinionAltaForma(prefix='opinion_jefe')
        formOpinionRH = OpinionAltaForma(prefix='opinion_rh', instance=opinion_rh[0]) if opinion_rh else OpinionAltaForma(prefix='opinion_rh')
        formInformante1 = InformanteAltaForma(prefix='informante1', instance=informante1) if informante1 else InformanteAltaForma(prefix='informante1')
        formInformante2 = InformanteAltaForma(prefix='informante2', instance=informante2) if informante2 else InformanteAltaForma(prefix='informante2')

        context['investigacion'] = investigacion
        context['trayectoria_empresa'] = trayectoria_empresa
        context['evaluacion'] = evaluacion[0] if evaluacion else None
        context['opinion_jefe'] = opinion_jefe[0] if opinion_jefe else None
        context['opinion_rh'] = opinion_rh[0] if opinion_rh else None
        context['carta_laboral'] = carta_laboral
        context['datos_generales'] = datos_generales
        context['informante1'] = informante1
        context['informante2'] = informante2
        context['datos_entrevista'] = datos_entrevista
        context['formSucursal'] = formSucursal
        context['formTrayectoria'] = formTrayectoria
        context['formCartaLaboral'] = formCartaLaboral
        context['formDatosGenerales'] = formDatosGenerales
        context['formEvaluacion'] = formEvaluacion
        context['formOpinionJefe'] = formOpinionJefe
        context['formOpinionRH'] = formOpinionRH
        context['formInformante1'] = formInformante1
        context['formInformante2'] = formInformante2


        return context