from django.conf.urls import include, url

from app.bitacora.views import panel, search_bitacora, reset_filtros

urlpatterns = [
	url(r'^$', panel, name='bitacora_panel'),

	#AJAX
	url(r'^search_bitacora/$', search_bitacora, name='search_bitacora'),
	url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_bitacora')
]
