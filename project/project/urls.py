from django.conf.urls import include, url
from django.urls import path
from django.conf import settings

from app.core.views.dash import DashboardView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    
    url(r'^', include('app.front.urls')),

    url(r'^api/', include('app.api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path("dash", DashboardView.as_view(), name="dashboard"),
    path("core/", include("app.core.urls")),
    path("clientes/", include("app.clientes.urls")),
    path("personas/", include("app.persona.urls")),
    path("investigaciones/", include("app.investigacion.urls")),
    path("pagos_a_gestores/", include("app.pagos_gestores.urls")),
]


if settings.SHOW_DJANGO_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    SHOW_TOOLBAR_CALLBACK = True
