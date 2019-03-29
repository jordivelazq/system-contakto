from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'app.cobranza.views.panel', name='panel_cobranza'),
	url(r'^exito/$', 'app.cobranza.views.panel', name='panel_cobranza'),
	url(r'^error/$', 'app.cobranza.views.panel', name='panel_cobranza'),
	# #AJAX
	url(r'^get_facturas/$', 'app.cobranza.views.get_facturas', name='get_facturas'),
	url(r'^get_facturas/compania/(?P<compania_id>[^/]+)/$', 'app.cobranza.views.get_facturas', name='get_facturas'),
	url(r'^get_facturas/contacto/(?P<contacto_id>[^/]+)/$', 'app.cobranza.views.get_facturas', name='get_facturas'),
	url(r'^get_facturas/compania/(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/$', 'app.cobranza.views.get_facturas', name='get_facturas'),
	url(r'^search_cobranza/$', 'app.cobranza.views.search_cobranza', name='search_cobranza'),
    url(r'^reset_filtros/$', 'app.cobranza.views.reset_filtros', name='reset_filtros_cobranza'),
)	

