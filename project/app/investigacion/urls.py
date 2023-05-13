from app.cobranza.new_views.cobranzas_investigaciones import InvestigacionFacturaViewSet
from app.investigacion.new_view.adjuntos import (
    InvestigacionAdjuntosDetailView,
    InvestigacionAdjuntosFormTemplateView,
    InvestigacionAdjuntosTemplateView,
    InvestigacionAdjuntosViewSet,
)
from app.investigacion.new_view.bitacoras import InvestigacionBitacoraCreateView
from app.investigacion.new_view.edicion_entrevista_persona import (
    EdicionEntrevistaEjecutivoVisitaTemplateView,
    EdicionEntrevistaPersonaTemplateView,
)
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import (
    CandidatoTemplateView,
    InvestigacionCandidatoTemplateView,
    InvestigacionCandidatoViewSet,
    InvestigacionCobranzasClienteCompletaComprobanteTemplateView,
    InvestigacionCobranzasCompletarFacturaTemplateView,
    InvestigacionCoodinadorVisitaDetailView,
    InvestigacionCoodinadorVisitaViewSet,
    InvestigacionCoordiandorVisitaTemplateView,
    InvestigacionCoordinadorCompletarAdjuntosTemplateView,
    InvestigacionCoordinadorCompletarEntrevistaTemplateView,
    InvestigacionCoordinadorCompletarInvLaboralTemplateView,
    InvestigacionCoordinadorCompletarTemplateView,
    InvestigacionCoordinadorDemandasCreateView,
    InvestigacionCoordinadorDemandasDeleteView,
    InvestigacionCoordinadorDemandasUpdateView,
    InvestigacionCoordinadorPsicometricoCreateView,
    InvestigacionCoordinadorPsicometricoDetailView,
    InvestigacionCoordinadorPsicometricoTemplateView,
    InvestigacionCoordinadorPsicometricoUpdateView,
    InvestigacionCoordinadorPsicometricoViewSet,
    InvestigacionCoordinadorVisitaCreateView,
    InvestigacionCoordinadorVisitaUpdateView,
    InvestigacionCoordPsicometricoUpdateView,
    InvestigacionCoordVisitaUpdateView,
    InvestigacionDetailView,
    InvestigacionEjecutivoDeCuentaUpdateView,
    InvestigacionEjecutivoLaboralCandidatoTemplateView,
    InvestigacionEjecutivoLaboralDetailView,
    InvestigacionEjecutivoLaboralTemplateView,
    InvestigacionEjecutivoLaboralViewSet,
    InvestigacionEjecutivoPsicometricoDetailView,
    InvestigacionEjecutivoPsicometricoList,
    InvestigacionEjecutivoPsicometricoUpdateView,
    InvestigacionEjecutivoVisitaTemplateView,
    InvestigacionEjecutivoVisitaUpdateView,
    InvestigacionEjecutivoVisitaViewSet,
    InvestigacionEntrevistaTemplateView,
    InvestigacionEntrevistaViewSet,
    InvestigacionTemplateView,
    InvestigacionUpdateView,
    InvestigacionViewSet,
    PersonaTrajectoriaComercialCrearTemplateView,
    PersonaTrajectoriaComercialDeleteTemplateView,
    PersonaTrayectoriaCrearTemplateView,
    PersonaTrayectoriaEditTemplateView,
    InvestigacionPersonaTrayectoriaLaboralDeleteTemplateView,
)

from .new_view.investigacion import InvestigacionCerrarUpdateView

router = DefaultRouter()
router.register(r"investigaciones", InvestigacionViewSet)
router.register(r"investigaciones_candidatos", InvestigacionCandidatoViewSet)
router.register(r"ejecutivo_de_cuentas", InvestigacionEjecutivoLaboralViewSet)
router.register(
    r"investigaciones_coordinador_visita", InvestigacionCoodinadorVisitaViewSet
)
router.register(
    r"investigaciones_ejecutivo_visita", InvestigacionEjecutivoVisitaViewSet
)
router.register(r"investigaciones_entrevista", InvestigacionEntrevistaViewSet)
router.register(
    r"investigaciones_psicometrico", InvestigacionCoordinadorPsicometricoViewSet
)
router.register(r"investigaciones_adjuntos", InvestigacionAdjuntosViewSet)
router.register(r"investigaciones_facturas", InvestigacionFacturaViewSet)

app_name = "investigaciones"


urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "investigaciones/",
        InvestigacionTemplateView.as_view(),
        name="investigaciones_list",
    ),
    path(
        "investigaciones/detail/<int:pk>/",
        InvestigacionDetailView.as_view(),
        name="investigacion_detail",
    ),
    path(
        "investigaciones/update/<int:pk>/",
        InvestigacionUpdateView.as_view(),
        name="investigacion_edit",
    ),
    path(
        "investigaciones/cerrar/<int:pk>/",
        InvestigacionCerrarUpdateView.as_view(),
        name="investigacion_cerrar",
    ),
    # edicion datos del candidato por parte del coordinado y el ejecutivo de venta
    path(
        "investigaciones/candidato/",
        InvestigacionCandidatoTemplateView.as_view(),
        name="investigaciones_candidato",
    ),
    path(
        "investigaciones/candidatos/<int:investigacion_id>/",
        CandidatoTemplateView.as_view(),
        name="investigacion_candidato_edit",
    ),
    path(
        "investigaciones/ejecutivo-de-ventas/candidatos/<int:investigacion_id>/",
        InvestigacionEjecutivoLaboralCandidatoTemplateView.as_view(),
        name="investigacion_edv_candidato_edit",
    ),
    # Trayectoria laboral
    path(
        "investigaciones/persona/trayectoria-laboral/create/<int:investigacion_id>/",
        PersonaTrayectoriaCrearTemplateView.as_view(),
        name="investigacion_persona_trayectoria_laboral_create",
    ),
    path(
        "investigaciones/persona/trayectoria-laboral/edit/<int:investigacion_id>/<int:pk>/",
        PersonaTrayectoriaEditTemplateView.as_view(),
        name="investigacion_persona_trayectoria_laboral_edit",
    ),
    # Trayectoria comercial
    path(
        "investigaciones/persona/trayectoria-comercial/create/<int:investigacion_id>/<int:trayectoria_id>/",
        PersonaTrajectoriaComercialCrearTemplateView.as_view(),
        name="investigacion_persona_trayectoria_comercial_create",
    ),
    path(
        "investigaciones/persona/trayectoria-comercial/delete/<int:investigacion_id>/<int:trayectoria_id>/<int:pk>/",
        PersonaTrajectoriaComercialDeleteTemplateView.as_view(),
        name="investigacion_persona_trayectoria_comercial_delete",
    ),
    # Coordinador de Ejecutivo Asignaciones Coordinador de visitas
    path(
        "investigaciones/coordinador_ejecutivo/update_coord_visita/<int:pk>/",
        InvestigacionCoordVisitaUpdateView.as_view(),
        name="investigaciones_coordinador_ejecutivo_update_coord_visita",
    ),
    # Coordinador de Ejecutivo Asignaciones Coordinador de psicometricos
    path(
        "investigaciones/coordinador_ejecutivo/update_coord_psicometrico/<int:pk>/",
        InvestigacionCoordPsicometricoUpdateView.as_view(),
        name="investigaciones_coordinador_ejecutivo_update_coord_psicometrico",
    ),
    # asignacion de ejecutivos de visitas
    path(
        "investigaciones/ejecutivo-visitas",
        InvestigacionEjecutivoVisitaTemplateView.as_view(),
        name="investigaciones_ejecutivo_visitas_list",
    ),
    path(
        "investigaciones/ejecutivo-visitas/detail/<str:seccion_entrevista>/<int:pk>/",
        EdicionEntrevistaEjecutivoVisitaTemplateView.as_view(),
        name="investigaciones_ejecutivo_visitas_detail",
    ),
    # Asignacion de ejecutivos de ventas
    path(
        "investigaciones/cood-atc-cliente/ejecutivo-de-cuentea/update/<int:pk>/",
        InvestigacionEjecutivoDeCuentaUpdateView.as_view(),
        name="investigaciones_coord_de_visitas_eject_venta_update",
    ),
    # Asignacion de coordinadores de visita
    path(
        "investigaciones/coordinador-visitas",
        InvestigacionCoordiandorVisitaTemplateView.as_view(),
        name="investigaciones_coordinador_visitas_list",
    ),
    path(
        "investigaciones/coordinador-visitas/detail/<int:pk>/",
        InvestigacionCoodinadorVisitaDetailView.as_view(),
        name="investigaciones_coordinador_visitas_detail",
    ),
    path(
        "investigaciones/coordinador-visitas/detail/<str:seccion_entrevista>/<int:pk>/",
        InvestigacionCoodinadorVisitaDetailView.as_view(),
        name="investigaciones_coordinador_visitas_detail",
    ),
    path(
        "investigaciones/coordinador-visitas/create/<int:investigacion_id>/",
        InvestigacionCoordinadorVisitaCreateView.as_view(),
        name="investigaciones_coordinador_visitas_create",
    ),
    path(
        "investigaciones/coordinador-visitas/ejecutivo/update/<int:pk>/",
        InvestigacionEjecutivoVisitaUpdateView.as_view(),
        name="investigaciones_ejecutivo_visitas_update",
    ),
    path(
        "investigaciones/coordinador-visitas/update/<int:investigacion_id>/<int:pk>/",
        InvestigacionCoordinadorVisitaUpdateView.as_view(),
        name="investigaciones_coordinador_visitas_update",
    ),
    # Llenado ciclo de psicometria
    path(
        "investigaciones/coordinador-psicometrico",
        InvestigacionCoordinadorPsicometricoTemplateView.as_view(),
        name="investigaciones_coordinador_psicometrico_list",
    ),
    path(
        "investigaciones/coordinador-psicometrico/detail/<int:pk>/",
        InvestigacionCoordinadorPsicometricoDetailView.as_view(),
        name="investigaciones_coordinador_psicometrico_detail",
    ),
    path(
        "investigaciones/coordinador-psicometrico/create/<int:investigacion_id>/",
        InvestigacionCoordinadorPsicometricoCreateView.as_view(),
        name="investigaciones_coordinador_psicometrico_create",
    ),
    path(
        "investigaciones/coordinador-psicometrico/update/<int:investigacion_id>/<int:pk>/",
        InvestigacionCoordinadorPsicometricoUpdateView.as_view(),
        name="investigaciones_coordinador_psicometrico_update",
    ),
    # Ejecutivo de psicometrico
    path(
        "investigaciones/ejecutivo-psicometrico",
        InvestigacionEjecutivoPsicometricoList.as_view(),
        name="investigaciones_ejecutivo_psicometrico_list",
    ),
    path(
        "investigaciones/ejecutivo-psicometrico/update/<int:investigacion_id>/<int:pk>/",
        InvestigacionEjecutivoPsicometricoUpdateView.as_view(),
        name="investigaciones_ejecutivo_psicometrico_update",
    ),
    path(
        "investigaciones/ejecutivo-psicometrico/detail/<int:investigacion_id>/<int:pk>/",
        InvestigacionEjecutivoPsicometricoDetailView.as_view(),
        name="investigaciones_ejecutivo_psicometrico_detail",
    ),
    # Ejecutivo de investigacion laboral
    path(
        "investigaciones/ejecutivo-de-cuenta",
        InvestigacionEjecutivoLaboralTemplateView.as_view(),
        name="investigaciones_ejecutivo_laboral_list",
    ),
    path(
        "investigaciones/ejecutivo-de-cuenta/detail/<int:pk>/",
        InvestigacionEjecutivoLaboralDetailView.as_view(),
        name="investigacion_ejecutivo_laboral_detail",
    ),
    # Entrevistas de investigaciones
    # Llenado del formulario de entrevistas
    path(
        "investigaciones/entrevista",
        InvestigacionEntrevistaTemplateView.as_view(),
        name="investigaciones_entrevista_list",
    ),
    path(
        "investigaciones/entrevistal/detail/<str:seccion_entrevista>/<int:investigacion_id>/",
        EdicionEntrevistaPersonaTemplateView.as_view(),
        name="investigaciones_entrevista_detail",
    ),
    # Adjuntos de Investigaciones
    path(
        "investigaciones/adjuntos",
        InvestigacionAdjuntosTemplateView.as_view(),
        name="investigaciones_adjuntos_list",
    ),
    path(
        "investigaciones/adjuntos/detail/<int:pk>/",
        InvestigacionAdjuntosDetailView.as_view(),
        name="investigaciones_adjuntos_detail",
    ),
    path(
        "investigaciones/adjuntos/detail/update/<int:investigacion_id>/",
        InvestigacionAdjuntosFormTemplateView.as_view(),
        name="investigaciones_adjuntos_update",
    ),
    # Demandas laborales
    path(
        "investigaciones/demandas/create/<int:investigacion_id>/",
        InvestigacionCoordinadorDemandasCreateView.as_view(),
        name="investigaciones_demanada_create",
    ),
    path(
        "investigaciones/demandas/update/<int:investigacion_id>/<int:pk>/",
        InvestigacionCoordinadorDemandasUpdateView.as_view(),
        name="investigaciones_demanada_update",
    ),
    path(
        "investigaciones/demandas/delete/<int:investigacion_id>/<int:pk>/",
        InvestigacionCoordinadorDemandasDeleteView.as_view(),
        name="investigaciones_demanada_delete",
    ),
    # Completar la investigacion
    path(
        "investigaciones/completar/<int:investigacion_id>/",
        InvestigacionCoordinadorCompletarTemplateView.as_view(),
        name="investigaciones_completar",
    ),
    path(
        "investigaciones/completar_inv_laboral/<int:investigacion_id>/",
        InvestigacionCoordinadorCompletarInvLaboralTemplateView.as_view(),
        name="investigaciones_completar_inv_laboral",
    ),
    path(
        "investigaciones/completar_entrevista/<int:investigacion_id>/",
        InvestigacionCoordinadorCompletarEntrevistaTemplateView.as_view(),
        name="investigaciones_completar_inv_laboral",
    ),
    path(
        "investigaciones/completar_adjuntos/<int:investigacion_id>/",
        InvestigacionCoordinadorCompletarAdjuntosTemplateView.as_view(),
        name="investigaciones_completar_adjuntos",
    ),
    path(
        "investigaciones/completar_factura/<int:investigacion_id>/",
        InvestigacionCobranzasCompletarFacturaTemplateView.as_view(),
        name="investigaciones_completar_factura",
    ),
    path(
        "investigaciones/completar_comprobante_factura/<int:investigacion_id>/",
        InvestigacionCobranzasClienteCompletaComprobanteTemplateView.as_view(),
        name="investigaciones_completar_comprobante",
    ),
    path(
        "investigaciones/persona/trayectoria-laboral/delete/<int:investigacion_id>/<int:pk>",
        InvestigacionPersonaTrayectoriaLaboralDeleteTemplateView.as_view(),
        name="investigaciones_persona_trayectoria_laboral_delete",
    ),
    # Bitacoras de investigaciones
    path(
        "investigaciones/bitacora/create/<int:investigacion_id>/<str:page>/",
        InvestigacionBitacoraCreateView.as_view(),
        name="investigaciones_bitacora_create",
    ),
]
