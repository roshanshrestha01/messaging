from django.conf.urls import patterns, url
from msgin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^compose/$' ,views.compose, name='compose'),
    url(r'^inbox/$' ,views.inbox, name='inbox'),
    url(r'^send/$' ,views.send, name='send'),
    url(r'^outbox/$' ,views.outbox, name='outbox'),
    # ex: /polls/5/
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)


