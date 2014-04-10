from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dogeapp.views.home', name='home'),
    url(r'^subscribe/', 'dogeapp.views.subscribe', name='subscribe'),
    url(r'^about/', 'dogeapp.views.about', name='about'),
    url(r'^contact/', 'dogeapp.views.contact', name='contact'),
    url(r'^delete/(?P<user_id>\d+)/$', 'dogeapp.views.delete_user', name='delete_user'),


    url(r'^loaderio-7686b7498e0e98b1b05d0726a02467ec.html/',
        TemplateView.as_view(template_name='loaderio-7686b7498e0e98b1b05d0726a02467ec.html'),
        name='loaderio'),

    url(r'^admin/', include(admin.site.urls)),
)
