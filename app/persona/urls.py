from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^/$', 'app.persona.views.panel', name='panel_persona'),
	url(r'^nuevo$', 'app.persona.views.crear', name='crear_persona'),
	url(r'^nuevo/exito$', 'app.persona.views.crear', name='crear_persona'),
	url(r'^exito$', 'app.persona.views.panel', name='panel_persona'),
	url(r'^(?P<investigacion_id>[^/]+)/eliminar$', 'app.persona.views.eliminar', name='eliminar_persona'),

	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar$', 'app.persona.views.editar', name='editar_persona'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/ver$', 'app.persona.views.editar', name='editar_persona'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/exito$', 'app.persona.views.editar', name='editar_persona'),


	url(r'^(?P<candidato_id>[^/]+)/investigacion/nueva$', 'app.persona.views.nueva_investigacion_candidato', name='nueva_investigacion_candidato'),

	#Trayectoria
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/nueva$', 'app.persona.views.nueva_trayectoria', name='nueva_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/nueva/empresa/(?P<empresa_id>[^/]+)$', 'app.persona.views.nueva_trayectoria', name='nueva_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/$', 'app.persona.views.ver_trayectoria', name='ver_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/exito/$', 'app.persona.views.ver_trayectoria', name='ver_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/ver/trayectoria/(?P<trayectoria_id>[^/]+)$', 'app.persona.views.editar_trayectoria_empresa', name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/trayectoria/(?P<trayectoria_id>[^/]+)$', 'app.persona.views.editar_trayectoria_empresa', name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/trayectoria/(?P<trayectoria_id>[^/]+)/exito$', 'app.persona.views.editar_trayectoria_empresa', name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/borrar/trayectoria/(?P<trayectoria_id>[^/]+)$', 'app.persona.views.borrar_trayectoria_empresa', name='borrar_trayectoria_empresa'),

	#Entrevista (excel)
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/$', 'app.entrevista.views.editar_entrevista', name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/exito$', 'app.entrevista.views.editar_entrevista', name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/cargar/$', 'app.entrevista.views.cargar_entrevista', name='cargar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/ver/(?P<seccion_entrevista>[-\w]+)/$', 'app.entrevista.views.editar_entrevista', name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/(?P<seccion_entrevista>[-\w]+)/$', 'app.entrevista.views.editar_entrevista', name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/(?P<seccion_entrevista>[-\w]+)/exito$', 'app.entrevista.views.editar_entrevista', name='editar_entrevista'),
	
	#Observaciones
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/observaciones$', 'app.persona.views.observaciones', name='ver_observaciones'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/observaciones/exito$', 'app.persona.views.observaciones', name='ver_observaciones'),

	#Reporte
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/reporte$', 'app.persona.views.ver_reporte', name='ver_reporte'),
	url(r'^investigacion/exportar/(?P<investigacion_id>[^/]+)/(?P<tipo_reporte>[-\w]+)$', 'app.investigacion.views.exportar_pdf', name='exportar_pdf'),

	#Adjuntos
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/$', 'app.adjuntos.views.panel_adjuntos', name='panel_adjuntos'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/exito$', 'app.adjuntos.views.panel_adjuntos', name='panel_adjuntos'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/editar$', 'app.adjuntos.views.editar_adjuntos', name='editar_adjuntos'),

	#AJAX
	url(r'^existencia/$', 'app.persona.views.existencia', name='existencia_candidato'),
	url(r'^search_candidatos/$', 'app.persona.views.search_candidatos', name='search_candidatos'),
	url(r'^reset_filtros/$', 'app.persona.views.reset_filtros', name='reset_filtros_candidatos'),
)	

'''
    url(r'^(?P<investigacion_id>[^/]+)/editar$', 'app.investigacion.views.editar', name='editar_investigacion'),
    url(r'^(?P<investigacion_id>[^/]+)/editar/(?P<seccion>[-\w]+)/$', 'app.investigacion.views.editar', name='editar_investigacion'),
'''
