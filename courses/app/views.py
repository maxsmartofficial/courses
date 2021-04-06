from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Course, Module, CourseInstance, ModuleInstance
from .forms import CourseSignUpForm, ModuleReviewForm

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
	sign_up_possible = not Course.objects.alreadySignedUp(c) # For user
	return(render(request, 'app/course.html', {"course": c, "modules": module_list, "form": form, "sign_up_possible": sign_up_possible}))
	
	
def course_sign_up(request):
	if request.method == "POST":
		form = CourseSignUpForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data['course']
			if Course.objects.alreadySignedUp(course): # For user
				# Not valid
				return(Http404)
			length = form.cleaned_data['length']
			course_instance = CourseInstance.objects.startNewCourseInstance(course, length)
			
			return(HttpResponseRedirect(reverse('my_courses_course', kwargs={"pk":course_instance.id})))
			
	else:
		return(Http404)
	
	return(render(request, 'app/signup.html', {"form": form, "course": course}))
	


def my_courses(request):
	# Get all courses for user
	course_instances = CourseInstance.objects.all()
	courses_not_completed = []
	courses_completed = []
	for c in course_instances:
		if CourseInstance.objects.is_completed(c): # For user
			courses_completed.append(c)
		else:
			courses_not_completed.append(c)
	courses_not_completed.sort(key=lambda c: CourseInstance.objects.getNextDeadline(c))
	courses_completed.sort(key=lambda c: CourseInstance.objects.getEndDate(c))
	
	courses = courses_not_completed + courses_completed
	
	return(render(request, 'app/my_courses.html', {"courses": courses}))


def my_courses_course(request, pk):
	# Get course instance
	course_instance = get_object_or_404(CourseInstance, id=pk)
	# Get module instances for course instance and user
	module_list = ModuleInstance.objects.filter(course_instance=course_instance).order_by('module__order')
	return(render(request, 'app/course_instance.html', {"course_instance": course_instance, "module_instances": module_list}))


def view_module(request, pk):
	# Get module instance for user
	module_instance = get_object_or_404(ModuleInstance, id=pk)
	form = ModuleReviewForm(initial={'module_instance':module_instance})
	return(render(request, 'app/module_instance.html', {"module_instance": module_instance, "form": form}))


def module_review(request):
	if request.method == "POST":
		form = ModuleReviewForm(request.POST)
		module_instance = get_object_or_404(ModuleInstance, pk=request.POST['module_instance'])
		if form.is_valid():
			form.save()

			return(HttpResponseRedirect(reverse('my_courses_course', kwargs={"pk": module_instance.course_instance.id})))

	else:
		return(HttpResponse404)
		
	return(render(request, 'app/review.html', {"form": form, "module_instance": module_instance}))
	



def my_modules(request):
	modules = ModuleInstance.objects.all()# For user
	
	# Sort modules
	modules_due = []
	# Find modules that are available and that aren't completed
	for m in modules:
		if m.is_due_soon():
			modules_due.append(m)
	modules_due.sort(key=lambda m: m.deadline)
	
	return(render(request, 'app/my_modules.html', {"modules_due": modules_due}))