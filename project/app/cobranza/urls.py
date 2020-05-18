from django.conf.urls import include, url

from app.cobranza.views import panel, generar_reporte, get_facturas, search_cobranza, reset_filtros, cobranza_investigacion, cobranza_facturas, eliminar_cobranza_investigacion

urlpatterns = [
	url(r'^/$', panel, name='panel_cobranza'),
	url(r'^exito/$', panel, name='panel_cobranza'),
	url(r'^error/$', panel, name='panel_cobranza'),
	url(r'^generar_reporte/$', generar_reporte, name='generar_reporte'),

	url(r'^facturas$', cobranza_facturas, name='cobranza_facturas'),
	url(r'^facturas/exito$', cobranza_facturas, name='cobranza_facturas'),
	url(r'^facturas/nueva$', cobranza_investigacion, name='cobranza_investigacion'),
	url(r'^factura/(?P<folio>[^/]+)/$', cobranza_investigacion, name='cobranza_investigacion'),
	url(r'^factura/(?P<folio>[^/]+)/eliminar$', eliminar_cobranza_investigacion, name='eliminar_cobranza_investigacion'),

	# #AJAX
	url(r'^get_facturas/$', get_facturas, name='get_facturas'),
	url(r'^get_facturas/compania/(?P<compania_id>[^/]+)/$', get_facturas, name='get_facturas'),
	url(r'^get_facturas/contacto/(?P<contacto_id>[^/]+)/$', get_facturas, name='get_facturas'),
	url(r'^get_facturas/compania/(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/$', get_facturas, name='get_facturas'),
	url(r'^search_cobranza/$', search_cobranza, name='search_cobranza'),
    url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_cobranza'),
]
