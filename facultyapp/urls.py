from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
#	url(r'^get_name', views.get_name, name='get_name'),
#	url(r'^get_location', views.get_location, name='get_location'),
	url(r'^get_candidate', views.get_candidate, name='get_candidate'),

]