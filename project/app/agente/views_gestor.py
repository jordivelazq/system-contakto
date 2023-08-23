from datetime import datetime

from app.agente.models import GestorInfo
from app.agente.views import is_email_valid
from app.bitacora.models import Bitacora
from app.compania.models import Compania
from app.investigacion.models import Investigacion
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext


@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def gestor_panel(request):
    page = 'gestor'
    gestores = GestorInfo.objects.all().values_list('usuario', flat=True)
    if request.GET.get('search') and request.GET.get('search') != '':
        gestores = gestores.filter(
            Q(telefono=request.GET.get('search')) | Q(usuario__username__icontains=request.GET.get('search')))
    users = User.objects.filter(id__in=gestores, is_active=True)

    # Temporal para SEARCH
    empresas_select = Compania.objects.filter(status=True, es_cliente=True).order_by('nombre')
    agentes_select = User.objects.filter(is_staff=True, is_active=True).exclude(
        username='info@mintitmedia.com').order_by('username')
    status_select = Investigacion.STATUS_GRAL_OPCIONES
    filtros_json = request.session.get('filtros_search_agente', None)

    if filtros_json != None and len(filtros_json['agente_id']):
        agente_seleccionado = User.objects.get(pk=filtros_json['agente_id'])
        investigaciones = Investigacion.objects.filter(status_active=True).order_by('candidato__nombre').filter(
            agente__id=filtros_json['agente_id'])

        if len(filtros_json['compania_id']):
            investigaciones = investigaciones.filter(Q(compania__id=filtros_json['compania_id']))
        if len(filtros_json['status_id']):
            investigaciones = investigaciones.filter(Q(status_general=filtros_json['status_id']))
        if len(filtros_json['fecha_inicio']) and len(filtros_json['fecha_final']):
            fecha_inicio_format = datetime.datetime.strptime(filtros_json['fecha_inicio'], '%d/%m/%y').strftime(
                '%Y-%m-%d')
            fecha_final_format = datetime.datetime.strptime(filtros_json['fecha_final'], '%d/%m/%y').strftime(
                '%Y-%m-%d')
            investigaciones = investigaciones.filter(fecha_recibido__range=(fecha_inicio_format, fecha_final_format))

    return render(request, 'sections/gestor/panel.html', locals(), RequestContext(request))


@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def gestor_nuevo(request):
    page = 'gestor'
    title = 'Crear nuevo gestor'
    msg_class = 'alert alert-danger'
    username = password = first_name = last_name = telefono = ''
    state = []
    user = ''
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        telefono = request.POST.get('telefono', '')
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        zona = request.POST.get('zona', '')
        estatus = request.POST.get('estatus', '')
        tipo_pago = request.POST.get('tipo_pago', '')
        if not is_email_valid(username) or password == '' or first_name == '' or last_name == '':
            state.append('Favor de llenar los campos marcados con rojo')
            required_fields = True
        else:
            is_username_taken = User.objects.filter(username=username).count()

            if not is_username_taken:
                user = User(username=username, first_name=first_name, last_name=last_name, email=username)
                user.set_password(password)
                user.is_staff = True
                user.save()
                GestorInfo(usuario=user, telefono=telefono, ciudad=ciudad, estado=estado, zona=zona, fecha_ingreso=datetime.now(), estatus=estatus, tipo_pago=tipo_pago).save()
                b = Bitacora(action='crear-gestor: ' + str(user), user=request.user)
                b.save()
                return HttpResponseRedirect('/agentes/gestor/exito')
            else:
                user_exists = True
                state.append('Este usuario ya está registrado, utilizar otro.')

    return render(request, 'sections/gestor/form.html', locals(), RequestContext(request))


'''
	this function is not longer required, this function is handled throw NG
'''


@login_required(login_url='/login', redirect_field_name=None)
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def gestor_editar(request, user_id):
    user = User.objects.get(id=user_id)

    if user.gestorinfo_set.all().count():
        gestor_info = user.gestorinfo_set.all()[0]
    else:
        gestor_info = GestorInfo(usuario=user)
        gestor_info.save()

    page = 'gestor'
    editar_agente = True
    state = []
    msg_class = 'alert alert-danger'
    url = '/agentes/gestor/' + str(user.id) + '/editar'
    title = 'Editar gestor: ' + str(user)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    telefono = gestor_info.telefono
    ciudad = gestor_info.ciudad
    estado = gestor_info.estado
    zona = gestor_info.zona
    estatus = gestor_info.estatus
    tipo_pago = gestor_info.tipo_pago
    enable_delete_agente = True
    # este el usuario mint admin
    if user.username == 'admin':
        return HttpResponseRedirect('/agentes/gestor/')
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        telefono = request.POST.get('telefono', '')
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        zona = request.POST.get('zona', '')
        estatus = request.POST.get('estatus', '')
        tipo_pago = request.POST.get('tipo_pago', '')
        if not is_email_valid(username) or first_name == '' or last_name == '':
            state.append('Favor de llenar los campos marcados con rojo')
            required_fields = True
        else:
            is_username_taken = User.objects.filter(username=username).exclude(id=user_id).count()

            if not is_username_taken:
                user.username = username
                user.email = username
                user.first_name = first_name
                user.last_name = last_name
                if len(password):
                    user.set_password(password)
                user.save()
                gestor_info.telefono = telefono
                gestor_info.ciudad = ciudad
                gestor_info.estado = estado
                gestor_info.zona = zona
                gestor_info.estatus = estatus
                gestor_info.tipo_pago = tipo_pago
                gestor_info.save()
                msg_class = 'alert alert-success'
                state = 'Usuario guardado exitósamente'
                b = Bitacora(action='editar-gestor: ' + str(user), user=request.user)
                b.save()
                return HttpResponseRedirect('/agentes/gestor/exito')
            else:
                user_exists = True
                state.append('Este usuario ya está registrado, utilizar otro.')

    return render(request, 'sections/gestor/form.html', locals(), RequestContext(request))
