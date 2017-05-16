from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from facultyapp import views
from django.conf import settings
#from django.conf import settings
from django.conf.urls.static import static
from facultyapp.admin import gf_app_site
from django.conf.urls import include, url
#from guestfaculty.admin import basic_site, advanced_site




urlpatterns = [
    #url(r'^application/logout/$', lambda x: HttpResponseRedirect('/Shibboleth.sso/Logout')),
    #<meta http-equiv="refresh" content="0; url=/Shibboleth.sso/Logout">
    url(r'^candidateapplication/', include(gf_app_site.urls)),
    #url(r'^gfapp/', include(basic_site.urls)),
    #url(r'^gfapp/', include(advanced_site.urls)),
    url(r'^application/', include(admin.site.urls)),
    url(r'^faculty/', include('facultyapp.urls')),
    url(r'^candidateapplication/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^candidateapplication/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^registration/', include('allauth.urls')),
    url(r'^accounts/login/$', lambda x: HttpResponseRedirect('/application/')),  # Redirect this to applications page directly	
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Guest Faculty Application'
