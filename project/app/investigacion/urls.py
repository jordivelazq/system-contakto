from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter



from .api import InvestigacionTemplateView, InvestigacionViewSet, InvestigacionUpdateView

router = DefaultRouter()
router.register(r'investigaciones', InvestigacionViewSet)

app_name = "investigaciones"


urlpatterns = [
	path("api/", include(router.urls)),

	path('investigaciones/', InvestigacionTemplateView.as_view(), name='investigaciones_list'),
	path('investigaciones/update/<int:pk>/', InvestigacionUpdateView.as_view(), name='investigacion_edit'),

]
