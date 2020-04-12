from django.conf.urls import include, url

from app.agente.views import panel, nuevo, editar, borrar, search_agentes, reset_filtros

urlpatterns = [
	url(r'^/$', panel, name='agent_panel'),
	url(r'^/exito$', panel, name='agent_panel'),
    url(r'^nuevo$', nuevo, name='agent_new'),
    url(r'^(?P<user_id>[^/]+)/editar$', editar, name='editar_agente'),
    url(r'^(?P<user_id>[^/]+)/borrar$', borrar, name='borrar_agente'),
    url(r'^search_agentes/$', search_agentes, name='search_agentes'),
    url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_agentes')
]
