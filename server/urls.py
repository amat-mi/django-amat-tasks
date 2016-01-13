# coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

# OAuth2 provider
urlpatterns += patterns('',
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
)

urlpatterns += patterns('',
    url(r'^tasks/', include('tasks.urls', namespace='tasks')),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
