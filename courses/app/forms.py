from django import forms
from .models import Course

LENGTH_CHOICES = (
	("short", "Quick"),
	("medium", "Standard"),
	("long", "Relaxed")
)

class CourseSignUpForm(forms.Form):

	course = forms.ModelChoiceField(required=True, 
				queryset=Course.objects.all(), widget=forms.HiddenInput())
	length = forms.ChoiceField(choices=LENGTH_CHOICES)