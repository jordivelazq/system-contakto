from django.contrib import admin
from app.compania.models import Compania, Contacto,  DireccionFiscal, RegimenFiscal


class CompaniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email',
                    'telefono_alt', 'role', 'rfc')
    search_fields = ['nombre', 'telefono', 'email', 'telefono_alt', 'rfc']


class RegimenFiscalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]


admin.site.register(Compania, CompaniaAdmin)
admin.site.register(Contacto)
admin.site.register(DireccionFiscal)
admin.site.register(RegimenFiscal, RegimenFiscalAdmin)
