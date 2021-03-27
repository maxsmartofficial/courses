from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('course/<slug:course_slug>', views.view_course, name='course')
]