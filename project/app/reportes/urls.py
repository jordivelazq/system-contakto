from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^/$', 'app.reportes.views.panel', name='panel_reportes'),
	url(r'^exito/$', 'app.reportes.views.panel', name='panel_reportes'),
	url(r'^error/$', 'app.reportes.views.panel', name='panel_reportes'),

	url(r'^exportar/$', 'app.reportes.views.exportar_pdf', name='exportar_pdf'),
	# #AJAX
	url(r'^search_reportes/$', 'app.reportes.views.search_reportes', name='search_reportes'),
    url(r'^reset_filtros/$', 'app.reportes.views.reset_filtros', name='reset_filtros_reportes'),
)	

