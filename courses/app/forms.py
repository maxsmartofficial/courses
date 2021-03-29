from django import forms
from .models import Course, ModuleReview

LENGTH_CHOICES = (
	("short", "Quick"),
	("medium", "Standard"),
	("long", "Relaxed")
)

class CourseSignUpForm(forms.Form):

	course = forms.ModelChoiceField(required=True, 
				queryset=Course.objects.all(), widget=forms.HiddenInput())
	length = forms.ChoiceField(choices=LENGTH_CHOICES)
	
class ModuleReviewForm(forms.ModelForm):
	
	class Meta:
		model = ModuleReview
		fields = ['module_instance', 'assignment_success', 'research_review', 'assignment_review']
		widgets = {'module_instance': forms.HiddenInput()}
		labels = {
			'assignment_success': "How well did you do in the assignment problems?",
			'research_review': "How did you find the quality of the research material?",
			'assignment_review': "How did you find the quality of the assignment material?",
		}