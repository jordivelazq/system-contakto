from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import (CandidatoTemplateView, GestorInvestigacionCreateView,
                  InvestigacionDetailView, InvestigacionTemplateView,
                  InvestigacionUpdateView, InvestigacionViewSet,
                  PersonaTrayectoriaCrearTemplateView,
                  PersonaTrayectoriaEditTemplateView)

router = DefaultRouter()
router.register(r'investigaciones', InvestigacionViewSet)

app_name = "investigaciones"


urlpatterns = [
	path("api/", include(router.urls)),

	path('investigaciones/', InvestigacionTemplateView.as_view(), name='investigaciones_list'),
	path('investigaciones/detail/<int:pk>/', InvestigacionDetailView.as_view(), name='investigacion_detail'),
	path('investigaciones/update/<int:pk>/', InvestigacionUpdateView.as_view(), name='investigacion_edit'),

	path('investigaciones/candidatos/<int:investigacion_id>/', CandidatoTemplateView.as_view(), name='investigacion_candidato_edit'),

	path('investigaciones/persona/trayectoria-laboral/create/<int:investigacion_id>/', 
	    PersonaTrayectoriaCrearTemplateView.as_view(), name='investigacion_persona_trayectoria_laboral_create'),

	path('investigaciones/persona/trayectoria-laboral/edit/<int:investigacion_id>/<int:pk>/', 
	    PersonaTrayectoriaEditTemplateView.as_view(), name='investigacion_persona_trayectoria_laboral_edit'),


]
