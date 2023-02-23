from app.clientes.forms.user_forms import UserChangeForm, UserCreationForm
from app.clientes.models import (ClienteSolicitud, ClienteSolicitudCandidato,
                                 ClienteTipoInvestigacion, ClienteUser)
from django.contrib import admin
from django.contrib.auth import admin as auth_admin


@admin.register(ClienteUser)
class ClienteUserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ('telefono', 'compania',)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["username"]


@admin.register(ClienteTipoInvestigacion)
class ClienteTipoInvestigacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_investigacion', 'costo')


@admin.register(ClienteSolicitud)
class ClienteSolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'enviado', 'fecha_solicitud',
                    'fecha_actualizacion', 'get_candidatos_count',
                    'get_candidatos_completados_count', 'observaciones')
    list_filter = ('enviado', 'fecha_solicitud', 'fecha_actualizacion')
    search_fields = ('cliente__user__username', 'cliente__user__first_name',
                     'cliente__user__last_name', 'cliente__user__email')


@admin.register(ClienteSolicitudCandidato)
class ClienteSolicitudCandidatoAdmin(admin.ModelAdmin):
    pass
