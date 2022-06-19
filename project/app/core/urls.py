from app.core.api import UserTemplateView, UserViewSet
from app.core.views.users import UserCreateView, UserDetailView, UserUpdateView, UserUpdatePasswdView

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = "core"

urlpatterns = [

    path("api/", include(router.urls)),
    path("list/", UserTemplateView.as_view(), name="users_list"),

    path("user/create/", UserCreateView.as_view(), name="users_create"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="users_update"),
    path("user/password/update/<int:pk>/", UserUpdatePasswdView.as_view(), name="users_password_update"),

]
