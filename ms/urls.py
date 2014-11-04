from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from msgin import views

urlpatterns = patterns('',
    url(r'^$', 'ms.views.home', name='home'),
    url(r'^message/', include('msgin.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^msgs/$', views.MessageList.as_view()),
    url(r'^msgs/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)