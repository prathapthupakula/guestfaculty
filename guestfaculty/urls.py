from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from facultyapp import views


from facultyapp.admin import gf_app_site



urlpatterns = [
    #url(r'^$', include('facultyapp.urls')),
	#url(r'^admin_tools/', include('admin_tools.urls')),
	#url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
	#url(r'^jet/', include('jet.urls', 'jet')), #jet theme URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faculty/', include('facultyapp.urls')),
    #url(r'^planning/', include('gfplan.urls')),
    #url(r'^application/$', lambda x: HttpResponseRedirect('/application/facultyapp/guestfacultycandidate/')),  # Redirect this to applications page directly
    url(r'^application/', include(gf_app_site.urls)),
    url(r'^application/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^application/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^registration/', include('allauth.urls')),
    url(r'^accounts/login/$', lambda x: HttpResponseRedirect('/application/')),  # Redirect this to applications page directly	
    #url(r'^$',include(gf_app_site.urls)),
    #url(r'', include('model_report.urls')),
    #url(r'^report_builder/', include('report_builder.urls')),
    #url(r'^reporting/', include('reporting.urls')),
    #url(r'^reports/', include('reportengine.urls')),
]

admin.site.site_header = 'Guest Faculty Administration'
