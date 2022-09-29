from django.conf.urls import include, url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from app.api.views import empresa_get_contactos, add_investigacion
from app.api.views_login import *
from app.api.views_mobile import *

router = DefaultRouter()
router.register(r'entrevista_persona/(?P<investigacion_id>\d+)', EntrevistaPersonaViewSet)
router.register(r'entrevista_persona/(?P<investigacion>\d+)', EntrevistaPersonaDataViewSet)
router.register(r'entrevista_academica', EntrevistaAcademicaViewSet)
router.register(r'entrevista_actividaddes_habitos', EntrevistaActividadesHabitosViewSet)
router.register(r'entrevista_aspecto_hogar', EntrevistaAspectoHogarViewSet)
router.register(r'entrevista_aspecto_automovil', EntrevistaAutomovilViewSet)
router.register(r'entrevista_aspecto_candidato', EntrevistaAspectoCandidatoViewSet)
router.register(r'entrevista_bienes_raices', EntrevistaBienesRaicesViewSet)
router.register(r'entrevista_cuenta_debito', EntrevistaCuentaDebitoViewSet)
router.register(r'entrevista_deuda_actual', EntrevistaDeudaActualViewSet)
router.register(r'entrevista_direccion', EntrevistaDireccionViewSet)
router.register(r'entrevista_distribucion_dimensiones', EntrevistaDistribucionDimensionesViewSet)
router.register(r'entrevista_documento_cotejado', EntrevistaDocumentoCotejadoViewSet)
router.register(r'entrevista_economica', EntrevistaEconomicaViewSet)
router.register(r'entrevista_grado_escolaridad', EntrevistaGradoEscolaridadViewSet)
router.register(r'entrevista_historia_en_empresa', EntrevistaHistorialEnEmpresaViewSet)
router.register(r'entrevista_info_personal', EntrevistaInfoPersonalViewSet)
router.register(r'entrevista_licencia', EntrevistaLicenciaViewSet)
router.register(r'entrevista_miembro_marco_familiar', EntrevistaMiembroMarcoFamiliarViewSet)
router.register(r'entrevista_origen', EntrevistaOrigenViewSet)
router.register(r'entrevista_otro_idioma', EntrevistaOtroIdiomaViewSet)
router.register(r'entrevista_propietario_vivienda', EntrevistaPropietarioViviendaViewSet)
router.register(r'entrevista_referencia', EntrevistaReferenciaViewSet)
router.register(r'entrevista_seguro', EntrevistaSeguroViewSet)
router.register(r'entrevista_situacion_vivienda', EntrevistaSituacionViviendaViewSet)
router.register(r'entrevista_salud', EntrevistaSaludViewSet)
router.register(r'entrevista_prestacion_vivienda', EntrevistaPrestacionViviendaViewSet)
router.register(r'entrevista_tarjeta_credito_comercial', EntrevistaTarjetaCreditoComercialViewSet)
router.register(r'entrevista_telefono', EntrevistaTelefonoViewSet)
router.register(r'entrevista_tipo_inmueble', EntrevistaTipoInmuebleViewSet)




urlpatterns = [
    path("entrevistas/", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),

    url(r'^empresa/(?P<empresa_id>[^/]+)/get_contactos$', empresa_get_contactos, name='empresa_get_contactos'),
    url(r'^investigacion$', add_investigacion, name='add_investigacion'),
    url(r'^auth/token/$', TokenView.as_view(), name='api-auth-token'),
    url(r'^investigacion/list/$', AsignacionInvestigacionApiView.as_view(), name='api-investigacion-list'),
    url(r'^investigacion/(?P<pk>[^/]+)/detalle/$', InvestigacionDetailApiView.as_view(), name='api-investigacion'),
    url(r'^investigacion/adjunto/upload/$', InvestigacionUploadImageApiView.as_view(), name='api-investigacion-adjunto-upload'),
    url(r'^forms/datosgenerales/fields/$', DatosGeneralesFormApiView.as_view(), name='api-forms-datosgenerales-fields'),
    
    url(r'^investigacion/verifica_entrevista_persona/(?P<investigacion_id>[^/]+)/', VerificaEntrevistaPersona.as_view(), name='api-verifica-entrevista-persona'),
    url(r'^investigacion/elimina_entrevista_persona/(?P<investigacion_id>[^/]+)/', EliminaEntrevistaPersona.as_view(), name='api-elimina-entrevista-persona'),
]
