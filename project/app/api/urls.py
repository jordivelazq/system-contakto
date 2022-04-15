from django.conf.urls import include, url

from app.api.views import empresa_get_contactos, add_investigacion
from app.api.views_login import *
from app.api.views_mobile import *

urlpatterns = [
    url(r'^empresa/(?P<empresa_id>[^/]+)/get_contactos$', empresa_get_contactos, name='empresa_get_contactos'),
    url(r'^investigacion$', add_investigacion, name='add_investigacion'),
    url(r'^auth/token/$', TokenView.as_view(), name='api-auth-token'),
    url(r'^investigacion/list/$', AsignacionInvestigacionApiView.as_view(), name='api-investigacion-list'),
    url(r'^investigacion/(?P<pk>[^/]+)/detalle/$', InvestigacionDetailApiView.as_view(), name='api-investigacion'),
    url(r'^investigacion/adjunto/upload/$', InvestigacionUploadImageApiView.as_view(), name='api-investigacion-adjunto-upload'),
    url(r'^forms/datosgenerales/fields/$', DatosGeneralesFormApiView.as_view(), name='api-forms-datosgenerales-fields'),
]
