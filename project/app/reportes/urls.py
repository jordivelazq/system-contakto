from django.conf.urls import url

from app.reportes.views import panel, search_reportes, reset_filtros, reporte_prueba

urlpatterns = [
	url(r'^$', panel, name='panel_reportes'),
	url(r'^exito/$', panel, name='panel_reportes'),
	url(r'^error/$', panel, name='panel_reportes'),

	url(r'^reporte-prueba/$', reporte_prueba, name='reporte_prueba'),

	# #AJAX
	url(r'^search_reportes/$', search_reportes, name='search_reportes'),
	url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_reportes'),
]
