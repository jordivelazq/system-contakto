from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^/$', 'app.compania.views.panel', name='compania_panel'),
	url(r'^/exito$', 'app.compania.views.panel', name='compania_exit'),
	url(r'^nueva/$', 'app.compania.views.nueva', name='compania_nueva'),
	url(r'^nueva/ref/(?P<investigacion_id>[^/]+)/$', 'app.compania.views.nueva', name='compania_nueva'),
	
	url(r'^(?P<compania_id>[^/]+)/editar$', 'app.compania.views.editar', name='compania_editar'),
	url(r'^(?P<compania_id>[^/]+)/editar/ref/(?P<investigacion_id>[^/]+)/(?P<trayectoria_id>[^/]+)$', 'app.compania.views.editar', name='compania_editar'),
	url(r'^(?P<compania_id>[^/]+)/borrar$', 'app.compania.views.borrar', name='compania_borrar'),

	url(r'^(?P<compania_id>[^/]+)/sucursales$', 'app.compania.views.sucursal_main', name='sucursal_main'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/nueva$', 'app.compania.views.sucursal_new', name='sucursal_new'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/(?P<sucursal_id>[^/]+)/editar$', 'app.compania.views.sucursal_edit', name='sucursal_edit'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/(?P<sucursal_id>[^/]+)/eliminar$', 'app.compania.views.sucursal_delete', name='sucursal_delete'),

	url(r'^(?P<compania_id>[^/]+)/contactos$', 'app.compania.views.contactos', name='contactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/contactos/exito$', 'app.compania.views.contactos', name='contactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo$', 'app.compania.views.contacto_nuevo', name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/exito$', 'app.compania.views.contacto_nuevo', name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/ref/(?P<investigacion_id>[^/]+)/exito$', 'app.compania.views.contacto_nuevo', name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/ref/(?P<investigacion_id>[^/]+)/$', 'app.compania.views.contacto_nuevo', name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/editar$', 'app.compania.views.contacto_editar', name='contacto_editar'),
	url(r'^(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/borrar$', 'app.compania.views.contacto_borrar', name='contacto_borrar'),

	url(r'^(?P<compania_id>[^/]+)/get_contactos$', 'app.compania.views.get_contactos', name='getcontactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/get_contactos/(?P<investigacion_id>[^/]+)$', 'app.compania.views.get_contactos', name='getcontactos_compania'),
	url(r'^search_empresas/$', 'app.compania.views.search_empresas', name='search_empresas'),
	url(r'^reset_filtros/$', 'app.compania.views.reset_filtros', name='reset_filtros_empresas'),
)
