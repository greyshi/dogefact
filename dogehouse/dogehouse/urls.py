from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dogeapp.views.home', name='home'),
    url(r'^create/', 'dogeapp.views.create', name='create'),

    url(r'^admin/', include(admin.site.urls)),
)
