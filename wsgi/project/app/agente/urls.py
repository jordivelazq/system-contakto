from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^/$', 'app.agente.views.panel', name='agent_panel'),
	url(r'^/exito$', 'app.agente.views.panel', name='agent_panel'),
    url(r'^nuevo$', 'app.agente.views.nuevo', name='agent_new'),
    url(r'^(?P<user_id>[^/]+)/editar$', 'app.agente.views.editar', name='editar_agente'),
    url(r'^(?P<user_id>[^/]+)/borrar$', 'app.agente.views.borrar', name='borrar_agente'),
    url(r'^search_agentes/$', 'app.agente.views.search_agentes', name='search_agentes'),
    url(r'^reset_filtros/$', 'app.agente.views.reset_filtros', name='reset_filtros_agentes'),
)
