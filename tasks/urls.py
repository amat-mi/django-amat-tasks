# coding: utf-8

from channels.channel import Channel
from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from tasks.views import DoitView, TaskView


router = SimpleRouter()

##### Elenco endpoints ################################

##### Aggiunta degli url ####################################
urlpatterns = patterns('',
    url(r'^', include(router.urls)),    
)

##### Views ################################
urlpatterns += patterns('',
   url(r'^doit/$',
        DoitView.as_view(), 
        name='doit'),    
   url(r'^as_view/$',
        Channel('as_view').as_view(), 
        name='as_view'),    

   url(r'^taskrun$',
        TaskView.as_view(), 
        name='taskrun'),    
)
