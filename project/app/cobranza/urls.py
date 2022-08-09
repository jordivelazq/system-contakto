from app.cobranza.new_views.cobranzas_investigaciones import (
    InvestigacionFacturaArchivosUpdateView, InvestigacionFacturaArchivosCreateView,
    InvestigacionFacturalDetailView, InvestigacionFacturaListView,
    InvestigacionFacturaUpdateView)
from app.cobranza.views import (cobranza_facturas, cobranza_investigacion,
                                eliminar_cobranza_investigacion,
                                generar_reporte, panel, reset_filtros,
                                search_cobranza)
from django.conf.urls import include, url
from django.urls import path

# app_name = "cobranza_app"

urlpatterns = [

    path('facturas/', 
         InvestigacionFacturaListView.as_view(), name='cobranza_facturas_list'),
    path('facturas/detail/<int:pk>/', 
         InvestigacionFacturalDetailView.as_view(), name='cobranza_facturas_detail'),
    path('facturas/update/<int:investigacion_id>/<int:pk>/', 
         InvestigacionFacturaUpdateView.as_view(), name='cobranza_facturas_update'),
    
	# archivos de facturas
	path('facturas/archivos/create/<int:investigacion_id>/', 
         InvestigacionFacturaArchivosCreateView.as_view(), name='cobranza_facturas_archivo_create'),
	path('facturas/archivos/update/<int:investigacion_id>/<int:pk>/', 
         InvestigacionFacturaArchivosUpdateView.as_view(), name='cobranza_facturas_archivo_update'),


	url(r'^$', panel, name='panel_cobranza'),
	url(r'^exito/$', panel, name='panel_cobranza'),
	url(r'^error/$', panel, name='panel_cobranza'),
	url(r'^generar_reporte/$', generar_reporte, name='generar_reporte'),

	url(r'^facturas$', cobranza_facturas, name='cobranza_facturas'),
	url(r'^facturas/exito$', cobranza_facturas, name='cobranza_facturas'),
	url(r'^facturas/nueva$', cobranza_investigacion, name='cobranza_investigacion'),
	url(r'^factura/(?P<folio>[^/]+)/$', cobranza_investigacion, name='cobranza_investigacion'),
	url(r'^factura/(?P<folio>[^/]+)/eliminar$', eliminar_cobranza_investigacion, name='eliminar_cobranza_investigacion'),

	# #AJAX
	url(r'^search_cobranza/$', search_cobranza, name='search_cobranza'),
    url(r'^reset_filtros/$', reset_filtros, name='reset_filtros_cobranza'),
]
