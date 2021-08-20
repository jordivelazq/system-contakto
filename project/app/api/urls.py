from django.conf.urls import include, url

from app.api.views import empresa_get_contactos, add_investigacion

urlpatterns = [
    url(r'^empresa/(?P<empresa_id>[^/]+)/get_contactos$', empresa_get_contactos, name='empresa_get_contactos'),
    url(r'^investigacion$', add_investigacion, name='add_investigacion'),
]
