# -*- coding: utf-8 -*-
from operator import inv
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from app.clientes.models import Cliente, ClienteSolicitud, ClienteSolicitudCandidato, ClienteUser
from app.core.models import Estado, Municipio
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from app.persona.models import Persona
from app.investigacion.models import Investigacion
from datetime import date


class InitialClient(LoginRequiredMixin, TemplateView):

    template_name = 'clientes/initial_test.html'

    def get_context_data(self, **kwargs):
        context = super(InitialClient, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class ClienteSolicitudListView(GroupRequiredMixin, ListView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitud
    paginate_by = 25

    context_object_name = "cliente_solicitudes"
    template_name = 'clientes/solicitudes/solicitudes_list.html'

    page = {
        'title': 'Solicitudes',
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudListView, self).get_context_data(**kwargs)

        context['page'] = self.page
        u = User.objects.get(id=self.request.user.pk)

        cliente_user = None
        try:
            cliente_user =  ClienteUser.objects.get(username=u.username)
        except ClienteUser.DoesNotExist:
            print('Error en cliente_user')
        
        context['uc'] = cliente_user

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


class ClienteSolicitudEnviarTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = [u"Client",]
    raise_exception = True

    template_name = ''

    page = {
        'title': 'Projects',
    }

    def get(self, request, **kwargs):
       
        solicitud = ClienteSolicitud.objects.get(pk=self.kwargs['solicitud_id'])
        candidatos_solicitud = ClienteSolicitudCandidato.objects.filter(cliente_solicitud_id=self.kwargs['solicitud_id'])
        today = date.today()

        # Tipo de investigaciones 
        # Laboral, 
        # Visita Domiciliaria (Enrevista), 
        # Psicometrica
        # Validacion de Demanda,
        # 
        # En Conjunto:
        # Socio económina= Laboral + Visita Domiciliaria
        # Visita Domiciliaria con demanda
        # Ojo: Todos tienen demanda


        # Asocuación de campos

        # Listado de candidato de la solicitud.
        # en Listado de candidatos tener estado por cada servico asociado
        '''
        De investiacacion

        agente  (Para el coordinador)
        solicitud = ClienteSolicitud
        candidato = Persona
        compania = Compania
        sucursal = Sucursales
        contacto = Contacto, on_delete=models.CASCADE
        fecha_recibido = DateField
        hora_recibido = CharField
        puesto = models.CharField(max_length=140)

        tipo_investigacion_status
        '''

        for candidato in candidatos_solicitud:

            
            # Buscar Candidato si no existe crearlo
            try:
                persona = Persona.objects.get(nss=candidato.nss, curp=candidato.curp)
                persona.estado_id = candidato.estado_id
                persona.municipio_id = candidato.municipio_id
                # persona.save()
            except Persona.DoesNotExist:
                persona = Persona()
                persona.nss = candidato.nss
                persona.nombre = candidato.nombre
                persona.apellido = candidato.apellido
                persona.email = candidato.email
                persona.curp = candidato.curp
                persona.estado_id = candidato.estado_id
                persona.municipio_id = candidato.municipio_id
                persona.save()
                print('##### Persona creada #####')
                print('Persona creada', persona.pk)
                

            if candidato.tipo_investigacion == 2:
                print('Crear solicitud para candidato')

                investigacion = Investigacion()
                #investigacion.agente = solicitud.cliente.user
                investigacion.cliente_solicitud = solicitud
                investigacion.candidato = persona
                investigacion.compania = solicitud.cliente.compania
                investigacion.tipo_investigacion_status = candidato.tipo_investigacion
                # Colocar fehca y hora de envio por parte del cliente
                # compania sucursa y contacto tomarlo de la compachia del cliente
                # colocar en el formulario del cliente la sucursal
                # investigacion.sucursal = solicitud.cliente.compania.sucursal
                # investigacion.contacto = candidato.cliente.contacto
                investigacion.save()
                print('##############################')
                print('Investigacion creada con el id: ' + str(investigacion.pk))

                # crear entrevista + adjuntos
                # Crear laboral
                # Enviar notificacion a cliente y coordinador de ejecutivos
                # Coordinador de ejecutivos puede listar las solicitudes para asignarlas
                # Ejecutivo puede asignar una solicitud a un ejecutivo
                # Ejecutivo puede ver las solicitudes asignadas
                # Ejecutivo puede ejectuta solicitud
                # Ejecutivo termina solicitud
                # Colocar el costo al tipo de investigacion (Referencia)

                # adicionales
                # Puede editar la informacion del candidato el coordinador y ejecutivo de inv. laboral
                # hasta DOMICILIO ACTUAL (Trabajo del ejecutivo, a traves de llamada con el candidato)
                # Guardar la bitacora de llamadas
                # Al estar lleno los datos se activa la invistigacion.
                # 
                # Demandas laborales el coordinador las llena. Toda investigacion lleva demana 

                # Quien auoriza la Entrevista
                # Enviado a entrevistador eliminar y colocar el gestor con popup de usuarios gestores
                # Colocar bitacora
                # Estatus: Atención y concluida

                # Calificación Final cuando todos los procesos estan concluido

                # Investigacion laboral la ejeuta el ejecutivo de inv. laboral
            
            if candidato.tipo_investigacion == 4:
                print('Crear psicometria para candidato')
                # Genera la sicometria
                # Coordinador de ejecutivos las asigna a un ejecutivo
                # Ejecutivo puede listar las sicometrias para asignarlas
                # Enviar notificacion a Ejecutico y coordinador de ejecutivos
                # Ejecutivo termina la sicometria
                # ejecutivo recibe notificacion de terminacion de sicometria

        # Para ir eliminando
        # Persona creada 26014
        # 
        # Crear solicitud para candidato
        # ##############################
        # Investigacion creada con el id: 25991
        # Crear solicitud para candidato
        # ##############################
        # Investigacion creada con el id: 25992    
        
        # cambiar la solicitud a enviada
        solicitud.enviado = True
        solicitud.save()
        messages.add_message(self.request, messages.SUCCESS, 'El solicitud ha sido enviada satisfactoriamente.')
        return redirect('clientes:clientes_solicitud_detail', pk=solicitud.pk,)


class ClienteSolicitudDeleteView(GroupRequiredMixin, DeleteView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitud
    template_name = 'clientes/solicitudes/solicitud_confirm_delete.html'
    success_url = reverse_lazy('clientes:clientes_solicitudes_list')

    page = {
        'title': 'Eliminar Solicitud',
        'subtitle': 'delete file'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudDeleteView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class ClienteSolicitudCandidatoCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitudCandidato
    template_name = 'clientes/solicitudes/candidatos/candidato_form.html'
    fields = ['nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud']


    page = {
        'title': 'Investor',
        'subtitle': 'add investor'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoCreateView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['solicitud_id'] = self.kwargs['solicitud_id']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.cliente_solicitud_id = self.kwargs['solicitud_id']
        self.object.save()

        return super(ClienteSolicitudCandidatoCreateView, self).form_valid(form)

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'El candidato ha sido creado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})



class ClienteSolicitudCandidatoUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitudCandidato
    template_name = 'clientes/solicitudes/candidatos/candidato_form.html'
    fields = ['nombre', 'apellido', 'nss', 'email', 'edad', 'curp', 'puesto', 'estado', 'municipio', 'tipo_investigacion', 'archivo_solicitud']

    page = {
        'title': 'Investor',
        'subtitle': 'update'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoUpdateView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['solicitud_id'] = self.kwargs['solicitud_id']
        return context

    # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'El candidato ha sido actualizado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})


class ClienteSolicitudCandidatoDeleteView(GroupRequiredMixin, DeleteView):

    # required
    group_required = [u"Admin", u"SuperAdmin"]
    raise_exception = True

    model = ClienteSolicitudCandidato
    template_name = 'clientes/solicitudes/candidatos/candidato_confirm_delete.html'
    
    page = {
        'title': 'Eliminar candidato de Solicitud',
        'subtitle': 'delete file'
    }

    def get_context_data(self, **kwargs):
        context = super(ClienteSolicitudCandidatoDeleteView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['solicitud'] = ClienteSolicitud.objects.get(pk=self.kwargs['solicitud_id'])

        return context
    
     # send the user back to their own page after a successful update
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'El candidato ha sido eliminado satisfactoriamente.')
        return reverse('clientes:clientes_solicitud_detail', kwargs={"pk": self.kwargs['solicitud_id']})


class MunicipiosView(View):

    def get(self, context, **response_kwargs):
        efe_key = self.kwargs['efe_key']
        # e = Estado.objects.get(efe_key=efe_key)
        municipios_list = Municipio.objects.filter(efe_key=efe_key).values('id', 'municipio',).order_by('-municipio')
        # municipios_list = Municipio.objects.all().values('catalog_key', 'efe_key', 'municipio',).order_by('-municipio')
        response = [r for r in municipios_list]

        return HttpResponse(json.dumps(response))