from django.conf.urls import url
from . import views 
from django.contrib.auth.views import login

app_name = 'things'

urlpatterns = [
	#/things/
	url(r'^$', views.index, name='index'),
	
	url(r'^register/$', views.register, name='register'),



	#/things/712
	url(r'^(?P<category_id>[0-9]+)/$', views.detail, name='detail'),

	#/things/thing/add/
	# url(r'^create_thing/$', views.create_thing, name='create_thing'),
    url(r'^(?P<category_id>[0-9]+)/create_thing/$', views.create_thing, name='create_thing'),


	#/things/thing/update/
	# url(r'thing/(?P<pk>[0-9]+)/$', views.ThingUpdate.as_view(), name='thing-update'),
	

	#/things/thing/delete/
	# url(r'thing/(?P<pk>[0-9]+)/delete/$', views.ThingDelete.as_view(), name='thing-delete'),

	url(r'^login_user/$', views.login_user, name='login_user'),
    
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^(?P<category_id>[0-9]+)/delete_category/$', views.delete_category, name='delete_category'),
    url(r'^(?P<category_id>[0-9]+)/delete_thing/(?P<thing_id>[0-9]+)/$', views.delete_thing, name='delete_thing'),
    url(r'^create_category/$', views.create_category, name='create_category'),
    url(r'^things/(?P<filter_by>[a-zA_Z]+)/$', views.things, name='things'),


]
