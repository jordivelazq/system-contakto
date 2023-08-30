from django.contrib import admin
from app.cobranza.models import Cobranza

class CobranzaAdmin(admin.ModelAdmin):
	list_display = ('id', 'investigacion', 'monto', 'folio', 'status_cobranza', 'last_modified')

admin.site.register(Cobranza, CobranzaAdmin)