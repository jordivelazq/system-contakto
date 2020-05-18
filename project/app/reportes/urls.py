from django.conf.urls import include, url

from app.reportes.views import panel, search_reportes, reset_filtros

urlpatterns = [
	url(r'^/$', panel, name='panel_reportes'),
	url(r'^exito/$', panel, name='panel_reportes'),
	url(r'^error/$', panel, name='panel_reportes'),

	# #AJAX
	url(r'^search_reportes/$', search_reportes, name='search_reportes'),
	url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_reportes'),
]
