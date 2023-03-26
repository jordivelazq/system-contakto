from django.contrib import admin
from app.investigacion.models import (
    Investigacion,
    InvestigacionFactura,
    Psicometrico,
    PsicometricoUser,
    GestorInvestigacion,
    GestorInvestigacionPago,
    GestorInvestigacionPagoInv,
)
from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm


@admin.register(Investigacion)
class InvestigacionAdmin(admin.ModelAdmin):
    list_display = ("id", "candidato", "puesto", "status_general")
    readonly_fields = [
        "agente",
        "ejecutivo_de_cuentas",
        "coordinador_visitas",
        "ejecutivo_visitas",
        "coordinador_psicometrico",
    ]
    # search_fields = ['name', 'telephone', 'email', 'telephone_b', 'rfc']
    # list_filer = ('role')


@admin.register(InvestigacionFactura)
class InvestigacionFacturaAdmin(admin.ModelAdmin):
    list_display = ("id", "investigacion", "cantidad", "descripcion", "monto")
    readonly_fields = [
        "investigacion",
    ]


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
    list_display = ("id", "user", "investigacion")
    readonly_fields = [
        "investigacion",
    ]


@admin.register(GestorInvestigacion)
class GestorInvestigacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gestor",
        "investigacion",
        "fecha_atencion",
        "pagado",
        "completado",
    )
    readonly_fields = [
        "investigacion",
    ]


class GestorInvestigacionPagoInvtLineInline(admin.TabularInline):
    model = GestorInvestigacionPagoInv
    # raw_id_fields = ("service",)
    readonly_fields = [
        "investigacion",
    ]


@admin.register(GestorInvestigacionPago)
class GestorInvestigacionPagoAdmin(admin.ModelAdmin):
    list_display = ("id", "gestor", "pagado", "comprobante")
    inlines = (GestorInvestigacionPagoInvtLineInline,)
