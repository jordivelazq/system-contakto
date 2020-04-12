from django.conf.urls import include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from app.front.views import panel, mint_login, mint_logout

urlpatterns = [
    url(r'^$', panel, name='panel'),
    
    url(r'^agentes', include('app.agente.urls')),
    url(r'^agente/', include('app.agente.urls')),

    url(r'^empresas', include('app.compania.urls')),
    url(r'^empresa/', include('app.compania.urls')),

    url(r'^candidatos', include('app.persona.urls')),
    url(r'^candidato/', include('app.persona.urls')),

    url(r'^bitacora', include('app.bitacora.urls')),
    url(r'^bitacora/', include('app.bitacora.urls')),

    url(r'^login$', mint_login),
    url(r'^logout$', mint_logout),

    url(r'^cobranza', include('app.cobranza.urls')),
    url(r'^cobranza/', include('app.cobranza.urls')),

    url(r'^estatus', include('app.reportes.urls')),
    url(r'^estatus/', include('app.reportes.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
