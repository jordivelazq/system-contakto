from django.contrib import admin
from app.investigacion.models import Investigacion, Psicometrico, PsicometricoUser
from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm


@admin.register(Investigacion)
class InvestigacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidato','puesto', 'status_general')
    readonly_fields = ["agente", 'ejecutivo_de_cuentas', 'coordinador_visitas', 'ejecutivo_visitas', 'coordinador_psicometrico']
    #search_fields = ['name', 'telephone', 'email', 'telephone_b', 'rfc']
    #list_filer = ('role')


@admin.register(PsicometricoUser)
class PsicometricoUserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["username", "first_name", "last_name"]


@admin.register(Psicometrico)
class PsicometricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'investigacion')
    readonly_fields = ["investigacion",]
