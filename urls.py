from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from connect4online.connect4.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'connect4online.views.home', name='home'),
    url(r'^$', home_login),
	# TODO: Make these URLs more RESTful
    url(r'^initialize_game/$', initialize_game),
    url(r'^get_challenger/$', get_challenger),
    url(r'^send_move/$', send_move),
    url(r'^get_turn/$', get_turn),

	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT,
		}),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
