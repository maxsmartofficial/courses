from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Course, Module, CourseInstance, ModuleInstance
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
	


def my_courses(request):
	# Get all courses for user
	course_instances = CourseInstance.objects.all()
	
	return(render(request, 'app/my_courses.html', {"courses":course_instances}))


def my_courses_course(request, pk):

	# Get course instance
	course_instance = get_object_or_404(CourseInstance, id=pk)
	# Get module instances for course instance and user
	module_list = ModuleInstance.objects.filter(course_instance=course_instance).order_by('module__order')
	return(render(request, 'app/course_instance.html', {"course_instance": course_instance, "module_instances": module_list}))


def view_module(request, pk):
	# Get module instance for user
	module_instance = get_object_or_404(ModuleInstance, id=pk)
	
	return(render(request, 'app/module_instance.html', {"module_instance": module_instance}))