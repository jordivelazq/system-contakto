from django.contrib import admin

from app.core.models import Estado, Municipio, TipoInvestigacionCosto, UserMessage


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ("efe_key", "estado")
    # inlines = [ServicioCostoAdicionalInline]


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("id", "efe_key", "municipio")
    # inlines = [ServicioCostoAdicionalInline]


@admin.register(TipoInvestigacionCosto)
class TipoInvestigacionCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_investigacion", "costo")
    # inlines = [ServicioCostoAdicionalInline]


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "user")

