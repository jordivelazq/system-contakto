from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import (CandidatoTemplateView, InvestigacionCandidatoTemplateView,
                  InvestigacionCandidatoViewSet,
                  InvestigacionCoodinadorVisitaDetailView,
                  InvestigacionCoodinadorVisitaViewSet,
                  InvestigacionCoordiandorVisitaTemplateView,
                  InvestigacionCoordinadorPsicometricoCreateView,
                  InvestigacionCoordinadorPsicometricoDetailView,
                  InvestigacionCoordinadorPsicometricoTemplateView,
                  InvestigacionCoordinadorPsicometricoUpdateView,
                  InvestigacionCoordinadorPsicometricoViewSet,
                  InvestigacionCoordinadorVisitaCreateView,
                  InvestigacionCoordinadorVisitaUpdateView,
                  InvestigacionCoordVisitaUpdateView, InvestigacionCoordPsicometricoUpdateView, InvestigacionDetailView,
                  InvestigacionEjecutivoLaboralDetailView,
                  InvestigacionEjecutivoLaboralTemplateView,
                  InvestigacionEjecutivoPsicometricoDetailView,
                  InvestigacionEjecutivoPsicometricoList,
                  InvestigacionEjecutivoPsicometricoUpdateView,
                  InvestigacionEntrevistaTemplateView,
                  InvestigacionEntrevistaViewSet, InvestigacionTemplateView,
                  InvestigacionUpdateView, InvestigacionViewSet,
                  PersonaTrajectoriaComercialCrearTemplateView,
                  PersonaTrajectoriaComercialDeleteTemplateView,
                  PersonaTrayectoriaCrearTemplateView,
                  PersonaTrayectoriaEditTemplateView)

router = DefaultRouter()
router.register(r'investigaciones', InvestigacionViewSet)
router.register(r'investigaciones_candidatos', InvestigacionCandidatoViewSet)
router.register(r'investigaciones_coordinador_visita', InvestigacionCoodinadorVisitaViewSet)
router.register(r'investigaciones_entrevista', InvestigacionEntrevistaViewSet)
router.register(r'investigaciones_psicometrico', InvestigacionCoordinadorPsicometricoViewSet)

app_name = "investigaciones"


urlpatterns = [
    path("api/", include(router.urls)),

    path('investigaciones/', 
         InvestigacionTemplateView.as_view(), name='investigaciones_list'),
    path('investigaciones/detail/<int:pk>/',
         InvestigacionDetailView.as_view(), name='investigacion_detail'),
    path('investigaciones/update/<int:pk>/',
         InvestigacionUpdateView.as_view(), name='investigacion_edit'),

    path('investigaciones/candidato/',
         InvestigacionCandidatoTemplateView.as_view(), name='investigaciones_candidato'),

    path('investigaciones/candidatos/<int:investigacion_id>/',
         CandidatoTemplateView.as_view(), name='investigacion_candidato_edit'),

    # Trayectoria laboral

    path('investigaciones/persona/trayectoria-laboral/create/<int:investigacion_id>/',
         PersonaTrayectoriaCrearTemplateView.as_view(),
         name='investigacion_persona_trayectoria_laboral_create'
         ),

    path('investigaciones/persona/trayectoria-laboral/edit/<int:investigacion_id>/<int:pk>/',
         PersonaTrayectoriaEditTemplateView.as_view(),
         name='investigacion_persona_trayectoria_laboral_edit'
         ),

    # Trayectoria comercial

    path('investigaciones/persona/trayectoria-comercial/create/<int:investigacion_id>/<int:trayectoria_id>/',
         PersonaTrajectoriaComercialCrearTemplateView.as_view(),
         name='investigacion_persona_trayectoria_comercial_create'
         ),

    path('investigaciones/persona/trayectoria-comercial/delete/<int:investigacion_id>/<int:trayectoria_id>/<int:pk>/',
         PersonaTrajectoriaComercialDeleteTemplateView.as_view(),
         name='investigacion_persona_trayectoria_comercial_delete'
         ),

    
    # Coordinador de Ejecutivo Asignaciones Coordinador de visitas
    path('investigaciones/coordinador_ejecutivo/update_coord_visita/<int:pk>/', 
         InvestigacionCoordVisitaUpdateView.as_view(), name='investigaciones_coordinador_ejecutivo_update_coord_visita'),

    # Coordinador de Ejecutivo Asignaciones Coordinador de psicometricos
    path('investigaciones/coordinador_ejecutivo/update_coord_psicometrico/<int:pk>/', 
         InvestigacionCoordPsicometricoUpdateView.as_view(), name='investigaciones_coordinador_ejecutivo_update_coord_psicometrico'),

    # Asignacion de coordinadores de visita
    path('investigaciones/coordinador-visitas', 
         InvestigacionCoordiandorVisitaTemplateView.as_view(), name='investigaciones_coordinador_visitas_list'),
    path('investigaciones/coordinador-visitas/detail/<int:pk>/',
         InvestigacionCoodinadorVisitaDetailView.as_view(), name='investigaciones_coordinador_visitas_detail'),
    path('investigaciones/coordinador-visitas/create/<int:investigacion_id>/',
         InvestigacionCoordinadorVisitaCreateView.as_view(), name='investigaciones_coordinador_visitas_create'),
    path('investigaciones/coordinador-visitas/create/<int:investigacion_id>/<int:pk>/',
         InvestigacionCoordinadorVisitaUpdateView.as_view(), name='investigaciones_coordinador_visitas_update'),

    # Llenado del formulario de entrevistas
    path('investigaciones/entrevista', InvestigacionEntrevistaTemplateView.as_view(),
         name='investigaciones_entrevista_list'),

    # Llenado ciclo de psicometria
    path('investigaciones/coordinador-psicometrico',
         InvestigacionCoordinadorPsicometricoTemplateView.as_view(), name='investigaciones_coordinador_psicometrico_list'),
    path('investigaciones/coordinador-psicometrico/detail/<int:pk>/',
         InvestigacionCoordinadorPsicometricoDetailView.as_view(), name='investigaciones_coordinador_psicometrico_detail'),
    path('investigaciones/coordinador-psicometrico/create/<int:investigacion_id>/',
         InvestigacionCoordinadorPsicometricoCreateView.as_view(), name='investigaciones_coordinador_psicometrico_create'),
    path('investigaciones/coordinador-psicometrico/update/<int:investigacion_id>/<int:pk>/',
         InvestigacionCoordinadorPsicometricoUpdateView.as_view(), name='investigaciones_coordinador_psicometrico_update'),

    # Ejecutivo de psicometrico

    path('investigaciones/ejecutivo-psicometrico',
         InvestigacionEjecutivoPsicometricoList.as_view(), name='investigaciones_ejecutivo_psicometrico_list'),
    path('investigaciones/ejecutivo-psicometrico/update/<int:investigacion_id>/<int:pk>/',
         InvestigacionEjecutivoPsicometricoUpdateView.as_view(), name='investigaciones_ejecutivo_psicometrico_update'),
    path('investigaciones/ejecutivo-psicometrico/detail/<int:investigacion_id>/<int:pk>/',
         InvestigacionEjecutivoPsicometricoDetailView.as_view(), name='investigaciones_ejecutivo_psicometrico_detail'),

    # Ejecutivo de investigacion laboral

    path('investigaciones/ejecutivo-laboral',
         InvestigacionEjecutivoLaboralTemplateView.as_view(), name='investigaciones_ejecutivo_laboral_list'),
	path('investigaciones/ejecutivo-laboral/detail/<int:pk>/',
         InvestigacionEjecutivoLaboralDetailView.as_view(), name='investigacion_ejecutivo_laboral_detail'),

]
