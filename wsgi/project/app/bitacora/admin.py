from django.contrib import admin
from app.bitacora.models import Bitacora

class BitacoraAdmin(admin.ModelAdmin):
	list_display = ('action', 'user', 'datetime')
	list_filter = ['action', 'user', 'datetime']

admin.site.register(Bitacora, BitacoraAdmin)

