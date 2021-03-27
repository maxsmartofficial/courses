from django.shortcuts import render
from django.http import HttpResponse

from .models import Course, Module

# Create your views here.

def index(request):
	# All available courses
	courses = Course.objects.all()
	
	return(render(request, 'app/index.html', {"courses": courses}))
	
def view_course(request, course_slug):
	# View details about a course
	c = Course.objects.get(slug=course_slug)
	module_list = Module.objects.filter(course=c).order_by('order')
	return(render(request, 'app/course.html', {"course": c, "modules": module_list}))
	
	