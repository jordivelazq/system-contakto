from django.conf.urls import url

from app.agente.views import panel, nuevo, editar, borrar, search_agentes, reset_filtros
from app.agente.views_gestor import gestor_panel, gestor_editar, gestor_nuevo
from app.agente.api import GestorInfoTemplateView, GestorInfoViewSet
from app.agente.new_views.gestores import GestorInfoCreateView, GestorInfoUpdateView, GestorInfoDeleteView

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'gestores', GestorInfoViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("list/", GestorInfoTemplateView.as_view(), name="gestor_info_list"),
    path("create/", GestorInfoCreateView.as_view(), name="gestor_info_create"),
    path("update/<int:pk>/", GestorInfoUpdateView.as_view(), name="gestor_info_update"),
    path("delete/<int:pk>/", GestorInfoDeleteView.as_view(), name="gestor_info_delete"),

	url(r'^$', panel, name='agent_panel'),
	url(r'^exito$', panel, name='agent_panel'),
    url(r'^nuevo$', nuevo, name='agent_new'),
    url(r'^(?P<user_id>[^/]+)/editar$', editar, name='editar_agente'),
    url(r'^(?P<user_id>[^/]+)/borrar$', borrar, name='borrar_agente'),
    url(r'^search_agentes$', search_agentes, name='search_agentes'),
    url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_agentes'),
    url(r'^gestor/$', gestor_panel, name='gestor_panel'),
    url(r'^gestor/exito$', gestor_panel, name='gestor_panel'),
    url(r'^gestor/nuevo$', gestor_nuevo, name='gestor_nuevo'),
    url(r'^gestor/(?P<user_id>[^/]+)/editar$', gestor_editar, name='gestor_editar'),

]
