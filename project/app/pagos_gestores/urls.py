from app.pagos_gestores.views.pagos_gestores import (
    GenerarPagoGestorTemplateView, GestoresInvestigacionDetsilTemplateView,
    GestoresInvestigacionListView,
    GestorInvestigacionPagoUpdateView, GestorInvestigacionPagoViewSet,
    GestorInvestigacionViewSet, GestoresInvestigacionPagosInvTemplateView)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'gestor_investigacion', GestorInvestigacionViewSet)
router.register(r'gestor_investifaciones_pagos', GestorInvestigacionPagoViewSet)

app_name = "pagos_gestores"

urlpatterns = [

    path("api/", include(router.urls)),
    path("list/", GestoresInvestigacionListView.as_view(), name="pagos_gestores_list"),
    path("detail/<int:gestor_id>/", GestoresInvestigacionDetsilTemplateView.as_view(), name="pagos_gestores_detail"),
    path("generar/pago/<int:gestor_id>/", GenerarPagoGestorTemplateView.as_view(), name="pagos_generar"),
    path("pago/update/<int:pk>/", GestorInvestigacionPagoUpdateView.as_view(), name="pagos_gestores_update"),

    path("pagados/list/", GestoresInvestigacionPagosInvTemplateView.as_view(), name="pagados_list"),


   
]
