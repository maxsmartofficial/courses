from django import forms
from .models import Course

class CourseSignUpForm(forms.Form):

	course = forms.ModelChoiceField(required=True, 
				queryset=Course.objects.all(), widget=forms.HiddenInput())