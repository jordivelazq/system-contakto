from django.conf.urls import include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.front.urls')),

    url(r'^api/', include('app.api.urls')),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    SHOW_TOOLBAR_CALLBACK = True
