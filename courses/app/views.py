from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Course, Module, CourseInstance
from .forms import CourseSignUpForm

# Create your views here.

def index(request):
	# All available courses
	courses = Course.objects.all()
	
	return(render(request, 'app/index.html', {"courses": courses}))
	
def view_course(request, course_slug):
	# View details about a course
	c = Course.objects.get(slug=course_slug)
	module_list = Module.objects.filter(course=c).order_by('order')
	form = CourseSignUpForm(initial={"course": c})
	return(render(request, 'app/course.html', {"course": c, "modules": module_list, "form": form}))
	
	
def course_sign_up(request):
	if request.method == "POST":
		form = CourseSignUpForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data['course']
			length = form.cleaned_data['length']
			CourseInstance.objects.startNewCourseInstance(course, length)
			
			return(HttpResponseRedirect(reverse('index', kwargs={})))
			
	else:
		return(HttpResponse404)
	
	return(render(request, 'app/signup.html', {"form": form}))
	

