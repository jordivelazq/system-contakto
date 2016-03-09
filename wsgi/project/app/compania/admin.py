from django.contrib import admin
from app.compania.models import Compania, Contacto

class CompaniaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'telefono', 'email', 'telefono_alt', 'role', 'rfc')
	search_fields = ['nombre', 'telefono', 'email', 'telefono_alt', 'rfc']
	#list_filer = ('role')

admin.site.register(Compania, CompaniaAdmin)
admin.site.register(Contacto)