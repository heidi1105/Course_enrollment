from django.conf.urls import url

from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^login', views.login),  #login process
	url(r'^register', views.register), #register process
	url(r'^dashboard', views.dashboard), #show courses of user (login first page)
	url(r'^createCourse', views.createCourse), #render to a page to put the name
	url(r'^creating', views.creating),  #creating course
	url(r'^enrollCourse', views.enrollCourse), # render to a page to enroll a course
	url(r'^enrolling/(?P<id>\d+)$', views.enrolling),
	url(r'^logout', views.logout),
	url(r'^drop/(?P<id>\d+)$', views.drop),
	url(r'^deleteCourse/(?P<id>\d+)$',views.deleteCourse)
]