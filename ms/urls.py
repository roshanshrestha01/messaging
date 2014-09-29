from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'ms.views.home', name='home'),
    url(r'^message/', include('msgin.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
