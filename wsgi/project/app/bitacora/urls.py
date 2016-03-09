from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^/$', 'app.bitacora.views.panel', name='bitacora_panel'),

	#AJAX
	url(r'^search_bitacora/$', 'app.bitacora.views.search_bitacora', name='search_bitacora'),
    url(r'^reset_filtros/$', 'app.bitacora.views.reset_filtros', name='reset_filtros_bitacora'),
)