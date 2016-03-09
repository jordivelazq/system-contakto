from django.contrib import admin
from app.persona.models import *

'''
class PersonAdmin(admin.ModelAdmin):
	list_display = ('name', 'nss', 'birth_date', 'email', 'address', 'phone_home', 'phone_cell', 'date_created')
	#search_fields = ['name', 'telephone', 'email', 'telephone_b', 'rfc']
	#list_filer = ('role')

class FileAdmin(admin.ModelAdmin):
	list_display = ('record', 'date_created')
'''

admin.site.register(Persona)
admin.site.register(Telefono)
admin.site.register(Direccion)
admin.site.register(PrestacionVivienda)
admin.site.register(Licencia)
admin.site.register(Origen)
admin.site.register(Legalidad)

admin.site.register(InfoPersonal)
admin.site.register(TrayectoriaLaboral)
admin.site.register(Salud)
admin.site.register(ActividadesHabitos)
admin.site.register(Academica)
admin.site.register(GradoEscolaridad)
admin.site.register(OtroIdioma)
admin.site.register(SituacionVivienda)
admin.site.register(PropietarioVivienda)
admin.site.register(CaractaristicasVivienda)
admin.site.register(TipoInmueble)
admin.site.register(DistribucionDimensiones)
admin.site.register(MiembroMarcoFamiliar)
admin.site.register(Economica)
admin.site.register(TarjetaCreditoComercial)
admin.site.register(CuentaDebito)
admin.site.register(Automovil)
admin.site.register(BienesRaices)
admin.site.register(Seguro)
admin.site.register(DeudaActual)
admin.site.register(Referencia)
admin.site.register(CuadroEvaluacion)
admin.site.register(DocumentoCotejado)
admin.site.register(AspectoHogar)
admin.site.register(AspectoCandidato)

admin.site.register(Evaluacion)
admin.site.register(Opinion)
admin.site.register(Informante)

admin.site.register(File)
