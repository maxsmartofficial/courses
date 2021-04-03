from django import template
from django.template.defaultfilters import stringfilter

from app.models import ModuleInstance, Course

import datetime
import markdown as md

register = template.Library()

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