from django.conf.urls import include, url

from app.agente.views import panel, nuevo, editar, borrar, search_agentes, reset_filtros
from app.agente.views_gestor import gestor_panel, gestor_editar, gestor_nuevo

urlpatterns = [
	url(r'^/$', panel, name='agent_panel'),
	url(r'^/exito$', panel, name='agent_panel'),
    url(r'^nuevo$', nuevo, name='agent_new'),
    url(r'^(?P<user_id>[^/]+)/editar$', editar, name='editar_agente'),
    url(r'^(?P<user_id>[^/]+)/borrar$', borrar, name='borrar_agente'),
    url(r'^search_agentes/$', search_agentes, name='search_agentes'),
    url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_agentes'),
    url(r'^/gestor/$', gestor_panel, name='gestor_panel'),
    url(r'^/gestor/exito$', gestor_panel, name='gestor_panel'),
    url(r'^/gestor/nuevo$', gestor_nuevo, name='gestor_nuevo'),
    url(r'^/gestor/(?P<user_id>[^/]+)/editar$', gestor_editar, name='gestor_editar'),

]
