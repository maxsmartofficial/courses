from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('course/<slug:course_slug>', views.view_course, name='course'),
	path('signup', views.course_sign_up, name='course_sign_up'),
	path('mycourses/', views.my_courses, name='my_courses'),
	path('mycourses/<uuid:pk>', views.my_courses_course, name='my_courses_course'),
	path('mycourses/module/<uuid:pk>', views.view_module, name='view_module'),
	path('review', views.module_review, name='module_review'),
]