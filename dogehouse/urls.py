from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dogeapp.views.home', name='home'),
    url(r'^subscribe/', 'dogeapp.views.subscribe', name='subscribe'),
    url(r'^about/', 'dogeapp.views.about', name='about'),
    url(r'^contact/', 'dogeapp.views.contact', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
)
