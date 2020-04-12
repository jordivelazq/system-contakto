from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.front.urls')),

    url(r'^api/', include('app.api.urls')),
    url(r'^admin/', include(admin.site.urls))
]
