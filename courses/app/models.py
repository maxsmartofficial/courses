from django.db import models

# Create your models here.
class Course(models.Model):
	
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=4000)
	short_description = models.TextField(max_length=200, null=True)
	slug = models.SlugField(max_length=200, null=True)
	
class Module(models.Model):
	
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=4000)
	short_description = models.TextField(max_length=200, null=True)
	order = models.IntegerField(default=0)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	
class Research(models.Model):

	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	text = models.TextField(max_length=40000)
	
class Assignment(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	text = models.TextField(max_length=40000)
	