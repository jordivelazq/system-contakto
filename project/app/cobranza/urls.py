from django.conf.urls import include, url
from django.urls import path

from app.cobranza.views import panel, generar_reporte, search_cobranza, reset_filtros, cobranza_investigacion, cobranza_facturas, eliminar_cobranza_investigacion

from app.cobranza.new_views.cobranzas import ClienteSolicitudesCanditatosFacturasListView, ClienteSolicitudDetaiFacturalView, ClienteSolicitudFacturaUpdateView

# app_name = "cobranza_app"

urlpatterns = [

    path('facturas/', 
         ClienteSolicitudesCanditatosFacturasListView.as_view(), name='cobranza_facturas_list'),
    path('facturas/detail/<int:pk>/', 
         ClienteSolicitudDetaiFacturalView.as_view(), name='cobranza_facturas_detail'),
    path('facturas/update/<int:solicitud_id>/<int:pk>/', 
         ClienteSolicitudFacturaUpdateView.as_view(), name='cobranza_facturas_update'),

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
