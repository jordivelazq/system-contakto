from django.contrib import admin
from app.investigacion.models import Investigacion


class InvestigacionAdmin(admin.ModelAdmin):
	list_display = ('id', 'candidato', 'status_general')
	#search_fields = ['name', 'telephone', 'email', 'telephone_b', 'rfc']
	#list_filer = ('role')


admin.site.register(Investigacion, InvestigacionAdmin)