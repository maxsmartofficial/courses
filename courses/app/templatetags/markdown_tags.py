from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
	return(md.markdown(value, extensions=['markdown.extensions.fenced_code']))
	
@register.filter()
@stringfilter
def markdown_sample(value):
	length = 80
	return(md.markdown(value[:length] + '...', extensions=['markdown.extensions.fenced_code']))