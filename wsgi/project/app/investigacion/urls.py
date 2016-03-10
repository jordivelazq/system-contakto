from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^nueva$', 'app.investigacion.views.nueva', name='investigacion_nueva'),
    url(r'^exito/(?P<candidato_id>[^/]+)$', 'app.investigacion.views.exito', name='investigacion_exito'),
    url(r'^/$', 'app.investigacion.views.panel', name='investigacion_panel'),
)
