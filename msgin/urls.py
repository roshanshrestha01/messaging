from django.conf.urls import patterns, url
from msgin import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^compose/(|(?P<msg_id>\d+)/)$',
                           views.compose,
                           name='compose'),
                       url(r'^edit/(?P<message_id>\d+)/$',
                           views.edit_message,
                           name='compose'),
                       url(r'^inbox/$', views.inbox, name='inbox'),
                       url(r'^send/$', views.send, name='send'),
                       url(r'^outbox/$', views.outbox, name='outbox'),
                       )
