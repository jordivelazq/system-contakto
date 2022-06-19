from django.contrib import admin

from app.core.models import Estado, Municipio

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('efe_key', 'estado')
    #inlines = [ServicioCostoAdicionalInline]


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'efe_key', 'municipio')
    #inlines = [ServicioCostoAdicionalInline]