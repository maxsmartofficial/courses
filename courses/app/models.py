from django.db import models
import uuid
import datetime

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
	
	def getTimeAllocated(self, length):
		if length=="short":
			days=4
		elif length=="medium":
			days=7
		elif length=="long":
			days=14
		else:
			raise Exception(length + " not a valid course length")
		return(60*60*24*days) # 7 days
	
class Research(models.Model):

	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	text = models.TextField(max_length=40000)
	
class Assignment(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	text = models.TextField(max_length=40000)


class CourseInstanceManager(models.Manager):
	def startNewCourseInstance(self, course, length):
		start_date = datetime.datetime.now()
		course_instance = CourseInstance(course=course, startdate = start_date)
		course_instance.save()
		# Create module instances
		modules = course.module_set.all().order_by('order')
		# Create first module instance - starting right now
		m = modules[0]
		startdate = start_date
		time = m.getTimeAllocated(length)
		deadline = startdate + datetime.timedelta(seconds = time)
		module_instance = ModuleInstance(course_instance=course_instance,
							module = m, startdate = startdate, deadline = deadline)
		module_instance.save()
		# Create other module instances - starting after previous deadline
		for i in range(1, len(modules)):
			m = modules[i]
			startdate = deadline
			time = m.getTimeAllocated(length)
			deadline = startdate + datetime.timedelta(seconds = time)
			module_instance = ModuleInstance(course_instance=course_instance,
								module = m, startdate = startdate, deadline = deadline)
			module_instance.save()


class CourseInstance(models.Model):
	# One of these is created every time the course is run - has many students
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	startdate = models.DateTimeField(null=True)
	
	objects = CourseInstanceManager()



class ModuleInstance(models.Model):
	# One of these is created for each student
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	course_instance = models.ForeignKey(CourseInstance, on_delete=models.CASCADE)
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	startdate = models.DateTimeField(null=True)
	deadline = models.DateTimeField(null=True)
	completed = models.BooleanField(default=False)
	
	def is_completed(self):
		return(hasattr(self, 'modulereview'))

	
	
class ModuleReview(models.Model):

	RESEARCH_CHOICES = (
		("NA","Not applicable."),
		("GG", "It was fine."),
		("TL", "It took too much time."),
		("TS", "There was too little content."),
		("TD", "I didn't understand it.")
	)

	ASSIGNMENT_CHOICES = (
		("NA","Not applicable."),
		("GG", "It was fine."),
		("TL", "It took too much time."),
		("TS", "There was too little content."),
		("TD", "I didn't understand it.")
	)
	
	SUCCESS_CHOICES = (
		("NA","Not applicable."),
		("GG", "I think I did very well."),
		("QG", "I think I mostly succeeded."),
		("QB", "I think I was mostly unsuccessful."),
		("BB", "I think I was completely unsuccessful.")
	)
	
	module_instance = models.OneToOneField(ModuleInstance, on_delete=models.SET_NULL, default=None, null=True, blank=True)
	assignment_success = models.CharField(max_length=2, choices = SUCCESS_CHOICES, default="NA")
	research_review = models.CharField(max_length=2, choices = RESEARCH_CHOICES, default="NA")
	assignment_review = models.CharField(max_length=2, choices = ASSIGNMENT_CHOICES, default="NA")
