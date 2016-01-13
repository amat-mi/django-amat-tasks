# coding: utf-8

from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from tasks.views import DoitView


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
)
