from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	#url(r'^/$', 'app.reportes.views.panel', name='panel_reportes'),
	
    url(r'^empresa/(?P<empresa_id>[^/]+)/get_contactos$', 'app.api.views.empresa_get_contactos', name='empresa_get_contactos'),

    url(r'^reporte/enviar_correo$', 'app.api.views.reporte_enviar_correo', name='reporte_enviar_correo'),
)	

