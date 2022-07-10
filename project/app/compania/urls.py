from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import CompaniaTemplateView, CompaniaViewSet
from .new_views.companias import (CompaniaCreateView, CompaniaDeleteView,
                                  CompaniaDetailView,
                                  CompaniaSucursalCreateView,
                                  CompaniaSucursalDeleteView,
                                  CompaniaSucursalUpdateView,
								  CompaniaContactoCreateView,
								  CompaniaContactoDeleteView,
								  CompaniaContactoUpdateView,
                                  CompaniaUpdateView)

router = DefaultRouter()
router.register(r'companias', CompaniaViewSet)


from app.compania.views import (borrar, contacto_borrar, contacto_editar,
                                contacto_nuevo, contactos, editar,
                                get_contactos, nueva, panel, reset_filtros,
                                search_empresas, sucursal_delete,
                                sucursal_edit, sucursal_main, sucursal_new)

urlpatterns = [

    path("api/", include(router.urls)),
    path("list/", CompaniaTemplateView.as_view(), name="companias_list"),
    path("detail/<int:pk>/", CompaniaDetailView.as_view(), name="companias_detail"),
    path("create/", CompaniaCreateView.as_view(), name="companias_create"),
    path("update/<int:pk>/", CompaniaUpdateView.as_view(), name="companias_update"),
    path("delete/<int:pk>/", CompaniaDeleteView.as_view(), name="companias_delete"),

    path("sucursal/create/<int:compania_id>/", CompaniaSucursalCreateView.as_view(), name="companias_sucursal_create"),
    path("sucursal/update/<int:compania_id>/<int:pk>/", CompaniaSucursalUpdateView.as_view(), name="companias_sucursal_update"),
    path("sucursal/delete/<int:compania_id>/<int:pk>/", CompaniaSucursalDeleteView.as_view(), name="companias_sucursal_delete"),

	path("contacto/create/<int:compania_id>/", CompaniaContactoCreateView.as_view(), name="companias_contacto_create"),
    path("contacto/update/<int:compania_id>/<int:pk>/", CompaniaContactoUpdateView.as_view(), name="companias_contacto_update"),
    path("contacto/delete/<int:compania_id>/<int:pk>/", CompaniaContactoDeleteView.as_view(), name="companias_contacto_delete"),


	url(r'^$', panel, name='compania_panel'),
	url(r'^exito$', panel, name='compania_exit'),
	url(r'^nueva/$', nueva, name='compania_nueva'),
	url(r'^nueva/ref/(?P<investigacion_id>[^/]+)/$', nueva, name='compania_nueva'),
	
	url(r'^(?P<compania_id>[^/]+)/editar$', editar, name='compania_editar'),
	url(r'^(?P<compania_id>[^/]+)/editar/ref/(?P<investigacion_id>[^/]+)/(?P<trayectoria_id>[^/]+)$', editar, name='compania_editar'),
	url(r'^(?P<compania_id>[^/]+)/borrar$', borrar, name='compania_borrar'),

	url(r'^(?P<compania_id>[^/]+)/sucursales$', sucursal_main, name='sucursal_main'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/nueva$', sucursal_new, name='sucursal_new'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/(?P<sucursal_id>[^/]+)/editar$', sucursal_edit, name='sucursal_edit'),
	url(r'^(?P<compania_id>[^/]+)/sucursal/(?P<sucursal_id>[^/]+)/eliminar$', sucursal_delete, name='sucursal_delete'),

	url(r'^(?P<compania_id>[^/]+)/contactos$', contactos, name='contactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/contactos/exito$', contactos, name='contactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo$', contacto_nuevo, name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/exito$', contacto_nuevo, name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/ref/(?P<investigacion_id>[^/]+)/exito$', contacto_nuevo, name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/nuevo/ref/(?P<investigacion_id>[^/]+)/$', contacto_nuevo, name='contacto_nuevo'),
	url(r'^(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/editar$', contacto_editar, name='contacto_editar'),
	url(r'^(?P<compania_id>[^/]+)/contacto/(?P<contacto_id>[^/]+)/borrar$', contacto_borrar, name='contacto_borrar'),

	url(r'^(?P<compania_id>[^/]+)/get_contactos$', get_contactos, name='getcontactos_compania'),
	url(r'^(?P<compania_id>[^/]+)/get_contactos/(?P<investigacion_id>[^/]+)$', get_contactos, name='getcontactos_compania'),
	url(r'^search_empresas/$', search_empresas, name='search_empresas'),
	url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_empresas')
]
