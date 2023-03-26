from app.cobranza.models import Cobranza
from django.contrib import admin


class CobranzaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investigacion",
        "monto",
        "folio",
        "status_cobranza",
        "last_modified",
    )


admin.site.register(Cobranza, CobranzaAdmin)
