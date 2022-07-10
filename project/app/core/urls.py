from app.core.api import UserTemplateView, UserViewSet
from app.core.views.users import UserCreateView, UserDetailView, UserUpdateView, UserUpdatePasswdView
from app.core.views.user_messages import UserMessajeListView, UserMessageDeleteView
from app.core.views.tipo_investigacion_costo import TipoInvestigacionCostoListView, TipoInvestigacionCostoCreateView,  TipoInvestigacionCostoUpdateView

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = "core"

urlpatterns = [

    path("api/", include(router.urls)),
    path("user_list/", UserTemplateView.as_view(), name="users_list"),

    path("user/create/", UserCreateView.as_view(), name="users_create"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="users_update"),
    path("user/password/update/<int:pk>/", UserUpdatePasswdView.as_view(), name="users_password_update"),

    path("tipo_investigacion_costo/", TipoInvestigacionCostoListView.as_view(), name="tipo_investigaciones_costo_list"),
    path("tipo_investigacion_costo/create/", TipoInvestigacionCostoCreateView.as_view(), name="tipo_investigacion_costo_create"),
    path("tipo_investigacion_costo/update/<int:pk>/", TipoInvestigacionCostoUpdateView.as_view(), name="tipo_investigacion_costo_update"),

    path('messages/list', UserMessajeListView.as_view(), name='user_messages_list'),
    path('messages/view/<int:pk>', UserMessageDeleteView.as_view(), name='user_messages_delete_list'),

]
