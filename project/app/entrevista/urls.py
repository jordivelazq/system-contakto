from app.clientes.api import ClienteTemplateView, ClienteUserViewSet


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .new_views.entrevistas import (EntrevistasTemplateView, EntrevistaInvestigacionViewSet)

router = DefaultRouter()
router.register(r'entrevistas', EntrevistaInvestigacionViewSet)


app_name = "entrevistas"

urlpatterns = [
    path("api/", include(router.urls)),
    path("list/", EntrevistasTemplateView.as_view(), name="entrevistas_list"),
]