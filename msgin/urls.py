from django.conf.urls import patterns, url
from msgin import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^compose/$',
                           views.compose,
                           name='compose'),
                       url(r'^(?P<msg_id>\d+)/$',
                           views.compose,
                           name='eidt_sch_msg'),
                       url(r'^inbox/$', views.inbox, name='inbox'),
                       url(r'^sent/$', views.sent, name='sent'),
                       url(r'^sent/usr/(?P<user_id>\d+)/$',
                           views.sent_msg_by_user,
                           name='sent_user_sepecify'),
                       url(r'^sent/grp/(?P<group_id>\d+)/$',
                           views.sent_msg_by_group,
                           name='sent_grp_sepecify'),
                       url(r'^outbox/$', views.outbox, name='outbox'),
                       url(r'^outbox/usr/(?P<user_id>\d+)/$',
                           views.messages_by_user,
                           name='user_sepecify'),
                       url(r'^outbox/grp/(?P<group_id>\d+)/$',
                           views.messages_by_group,
                           name='grp_sepecify'),

                       )
