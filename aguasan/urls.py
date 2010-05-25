from django.conf.urls.defaults import *
import settings
from os import path as os_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^aguasan/', include('aguasan.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('mapeo.urls')),
    (r'^$', 'mapeo.views.index'),
    (r'^cuenta/login/$', 'django.contrib.auth.views.login', {'template_name': 'usuarios/login.html'}),
    (r'^cuenta/cambiar-pass/$', 'django.contrib.auth.views.password_change',
                {'template_name': 'usuarios/password_change.html',
                 'post_change_redirect': '/'}),
    (r'^cuenta/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^archivos/(.*)$', 'django.views.static.serve',
                             {'document_root': os_path.join(settings.MEDIA_ROOT)}),
                           )
