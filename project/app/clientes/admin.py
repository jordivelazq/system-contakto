from app.clientes.forms import UserChangeForm, UserCreationForm
from app.clientes.models import (ClienteSolicitud,
                                 ClienteSolicitudCandidato)
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from app.clientes.models import ClienteUser


@admin.register(ClienteUser)
class ClienteUserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ('telefono', 'compania',)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["username"]


# @admin.register(Cliente)
# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('user', 'telefono', 'compania')
#     #inlines = [ServicioCostoAdicionalInline]


@admin.register(ClienteSolicitud)
class ClienteSolicitudAdmin(admin.ModelAdmin):
    pass
    # list_display = ('catalog_key', 'efe_key', 'municipio')
    #inlines = [ServicioCostoAdicionalInline]


@admin.register(ClienteSolicitudCandidato)
class ClienteSolicitudCandidatoAdmin(admin.ModelAdmin):
    pass
    # list_display = ('catalog_key', 'efe_key', 'municipio')
