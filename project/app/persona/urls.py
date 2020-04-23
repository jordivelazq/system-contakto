from django.conf.urls import include, url

from app.persona.views import panel, crear, eliminar, editar, nueva_trayectoria, ver_trayectoria, editar_trayectoria_empresa, borrar_trayectoria_empresa, trayectoria_comercial, trayectoria_comercial_borrar, trayectoria_comercial_referencia_borrar, observaciones, ver_reporte, existencia, search_candidatos, reset_filtros
from app.entrevista.views import editar_entrevista, cargar_entrevista
from app.investigacion.views import print_reporte_laboral, print_reporte_socioeconomico, print_reporte_visita_domiciliaria, print_reporte_validacion_demandas
from app.adjuntos.views import panel_adjuntos, editar_adjuntos


urlpatterns = [
	url(r'^/$', panel, name='panel_persona'),
	url(r'^nuevo$', crear, name='crear_persona'),
	url(r'^nuevo/exito$', crear, name='crear_persona'),
	url(r'^exito$', panel, name='panel_persona'),
	url(r'^(?P<investigacion_id>[^/]+)/eliminar$', eliminar, name='eliminar_persona'),

	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar$', editar, name='editar_persona'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/ver$', editar, name='editar_persona'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/exito$', editar, name='editar_persona'),

	#Trayectoria
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/nueva$', nueva_trayectoria, name='nueva_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/nueva/empresa/(?P<empresa_id>[^/]+)$', nueva_trayectoria, name='nueva_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/$', ver_trayectoria, name='ver_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/exito/$', ver_trayectoria, name='ver_trayectoria'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/ver/trayectoria/(?P<trayectoria_id>[^/]+)$', editar_trayectoria_empresa, name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/trayectoria/(?P<trayectoria_id>[^/]+)$', editar_trayectoria_empresa, name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/editar/trayectoria/(?P<trayectoria_id>[^/]+)/exito$', editar_trayectoria_empresa, name='editar_trayectoria_empresa'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/borrar/trayectoria/(?P<trayectoria_id>[^/]+)$', borrar_trayectoria_empresa, name='borrar_trayectoria_empresa'),

	#Referencia comercial
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/comercial/nueva$', trayectoria_comercial, name='trayectoria_comercial'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/comercial/(?P<trayectoria_id>[^/]+)$', trayectoria_comercial, name='trayectoria_comercial'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/comercial/(?P<trayectoria_id>[^/]+)/borrar$', trayectoria_comercial_borrar, name='trayectoria_comercial_borrar'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/trayectoria/comercial/(?P<trayectoria_id>[^/]+)/referencia/(?P<referencia_id>[^/]+)/borrar$', trayectoria_comercial_referencia_borrar, name='trayectoria_comercial_referencia_borrar'),

	#Entrevista (excel)
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/$', editar_entrevista, name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/exito$', editar_entrevista, name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/cargar/$', cargar_entrevista, name='cargar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/ver/(?P<seccion_entrevista>[-\w]+)/$', editar_entrevista, name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/(?P<seccion_entrevista>[-\w]+)/$', editar_entrevista, name='editar_entrevista'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/entrevista/editar/(?P<seccion_entrevista>[-\w]+)/exito$', editar_entrevista, name='editar_entrevista'),

	#Observaciones
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/observaciones$', observaciones, name='ver_observaciones'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/observaciones/exito$', observaciones, name='ver_observaciones'),

	#Reporte
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/reporte$', ver_reporte, name='ver_reporte'),
	url(r'^investigacion/exportar/reporte-laboral/(?P<investigacion_id>[^/]+)$', print_reporte_laboral, name='print_reporte_laboral'),
	url(r'^investigacion/exportar/reporte-socioeconomico/(?P<investigacion_id>[^/]+)$', print_reporte_socioeconomico, name='print_reporte_socioeconomico'),
	url(r'^investigacion/exportar/reporte-visita-domiciliaria/(?P<investigacion_id>[^/]+)$', print_reporte_visita_domiciliaria, name='print_reporte_visita_domiciliaria'),
	url(r'^investigacion/exportar/reporte-demandas/(?P<investigacion_id>[^/]+)$', print_reporte_validacion_demandas, name='print_reporte_validacion_demandas'),

	#Adjuntos
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/$', panel_adjuntos, name='panel_adjuntos'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/exito$', panel_adjuntos, name='panel_adjuntos'),
	url(r'^investigacion/(?P<investigacion_id>[^/]+)/adjuntos/editar$', editar_adjuntos, name='editar_adjuntos'),

	#AJAX
	url(r'^existencia/$', existencia, name='existencia_candidato'),
	url(r'^search_candidatos/$', search_candidatos, name='search_candidatos'),
	url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_candidatos')
]
