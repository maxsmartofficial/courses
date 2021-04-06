from django import template
from django.template.defaultfilters import stringfilter

from app.models import ModuleInstance, Course, CourseInstance

import datetime
import markdown as md

register = template.Library()

@register.simple_tag
def course_is_completed(course_instance):
	return(CourseInstance.objects.is_completed(course_instance))
	
@register.simple_tag
def total_completed_modules(course_instance):
	return(CourseInstance.objects.completed_modules(course_instance))

@register.simple_tag
def get_course_end_date(course_instance):
	endDate = CourseInstance.objects.getEndDate(course_instance)
	return(endDate)

@register.simple_tag
def get_next_deadline(course_instance):
	deadline = CourseInstance.objects.getNextDeadline(course_instance)
	return(deadline)

@register.simple_tag
def course_module_count(course):
	return(Course.objects.totalCourseModules(course))

@register.simple_tag
def count_modules():
	return(ModuleInstance.objects.getTotalModulesDue())

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