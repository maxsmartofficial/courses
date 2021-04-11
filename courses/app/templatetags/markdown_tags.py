from django import template
from django.template.defaultfilters import stringfilter

from app.models import ModuleInstance, Course, CourseInstance

import datetime
import markdown as md

register = template.Library()

@register.simple_tag
def course_is_completed(course_instance, user):
	student = user.student
	return(CourseInstance.objects.is_completed(course_instance, student))
	
@register.simple_tag
def total_completed_modules(course_instance, user):
	student = user.student
	return(CourseInstance.objects.completed_modules(course_instance, student))

@register.simple_tag
def get_course_end_date(course_instance, user):
	student = user.student
	endDate = CourseInstance.objects.getEndDate(course_instance, student)
	return(endDate)

@register.simple_tag
def get_next_deadline(course_instance, user):
	student = user.student
	deadline = CourseInstance.objects.getNextDeadline(course_instance, student)
	return(deadline)

@register.simple_tag
def course_module_count(course):
	return(Course.objects.totalCourseModules(course))

@register.simple_tag
def count_modules(user):
	student = user.student
	return(ModuleInstance.objects.getTotalModulesDue(student))

@register.filter()
def inthepast(date):
	return(date.astimezone() < datetime.datetime.now().astimezone())

@register.filter()
@stringfilter
def markdown(value):
	return(md.markdown(value, extensions=['markdown.extensions.fenced_code']))
	
@register.filter()
@stringfilter
def markdown_sample(value):
	length = 80
	return(md.markdown(value[:length] + '...', extensions=['markdown.extensions.fenced_code']))