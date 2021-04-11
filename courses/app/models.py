from django.db import models
import uuid
import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CourseManager(models.Manager):
	def totalCourseModules(self, course):
		return(Module.objects.filter(course=course).count())
		
	def alreadySignedUp(self, course): # For user
		incomplete = CourseInstance.objects.allIncompletedCourseInstances(course)
		return(len(incomplete) != 0)
			

class Course(models.Model):
	
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=4000)
	short_description = models.TextField(max_length=200, null=True)
	slug = models.SlugField(max_length=200, null=True)
	
	objects = CourseManager()
	
	def __str__(self):
		return(self.name)
	
class Module(models.Model):
	
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=4000)
	short_description = models.TextField(max_length=200, null=True)
	order = models.IntegerField(default=0)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	
	def __str__(self):
		return(self.name + ' | ' + str(self.course))
	
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
	
	def __str__(self):
		return(str(self.module))
	
class Assignment(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	text = models.TextField(max_length=40000)

	def __str__(self):
		return(str(self.module))

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
			
		return(course_instance)
		
	def getModules(self, course_instance): # For user
		"""Get ordered module instances for a course_instance"""
		return(ModuleInstance.objects.filter(course_instance=course_instance).order_by('module__order'))
		
		
	def previousModuleCompleted(self, module_instance): # For user
		"""Return True if the previous module is completed, or if it's the first module"""
		course_instance = module_instance.course_instance
		module_list = list(self.getModules(course_instance))
		index = module_list.index(module_instance)
		if index == 0:
			return(True)
		else:
			return(module_list[index - 1].is_completed())
			
	def getNextDeadline(self, course_instance): # For user
		module_instances = self.getModules(course_instance)
		nextDeadline = None
		for m in module_instances:
			if not m.is_completed():
				deadline = m.deadline
				if nextDeadline == None or nextDeadline > deadline:
					nextDeadline = deadline
		return(nextDeadline)
		
	def getEndDate(self, course_instance): # For user because getModules needs user although could change this
		modules = self.getModules(course_instance)
		endDate = max([m.deadline for m in modules])
		return(endDate)
		
	def is_completed(self, course_instance): # For user
		# Return True if all modules are completed
		modules = self.getModules(course_instance)
		all_complete = True
		for m in modules:
			if not m.is_completed():
				all_complete = False
		return(all_complete)
		
	def completed_modules(self, course_instance): # For user
		modules = self.getModules(course_instance)
		number_complete = 0
		for m in modules:
			if m.is_completed():
				number_complete += 1
		return(number_complete)
		
	def allCourseInstances(self, course): # For user
		course_instances = super().filter(course=course)
		return(course_instances)
		
	def allIncompletedCourseInstances(self, course): # For user
		course_instances = self.allCourseInstances(course)
		incomplete = []
		for c in course_instances:
			if not CourseInstance.objects.is_completed(c):
				incomplete.append(c)
		return(incomplete)


class ModuleInstanceManager(models.Manager):
	def getTotalModulesDue(self): # For user
		total = 0
		all_modules = super().all()
		for m in all_modules:
			if m.is_due_soon():
				total += 1
		return(total)


class CourseInstance(models.Model):
	# One of these is created every time the course is run - has many students
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	startdate = models.DateTimeField(null=True)
	
	objects = CourseInstanceManager()
	
	def __str__(self):
		return(str(self.course) + ' | ' + str(self.startdate))
	
	def is_completed(self): # For user
		# Return True if all modules are completed
		#modules = CourseInstance.objects.getModules(self)
		#all_complete = True
		for m in modules:
			if not m.is_completed():
				all_complete = False
		return(all_complete)
		
	def completed_modules(self): # For user
		#modules = CourseInstance.objects.getModules(self)
		#number_complete = 0
		for m in modules:
			if m.is_completed():
				number_complete += 1
		return(number_complete)
		


class ModuleInstance(models.Model):
	# One of these is created for each student
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	course_instance = models.ForeignKey(CourseInstance, on_delete=models.CASCADE)
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	startdate = models.DateTimeField(null=True)
	deadline = models.DateTimeField(null=True)
	completed = models.BooleanField(default=False)
	
	objects = ModuleInstanceManager()
	
	def __str__(self):
		return(str(self.module) + ' | ' + str(self.startdate))
	
	def is_completed(self):
		# Completed if there is a module review
		return(hasattr(self, 'modulereview'))
		
	def is_available(self):
		# Available if it is past the startdate or the previous module is completed
		if CourseInstance.objects.previousModuleCompleted(self):
			return(True)
		else:
			now = datetime.datetime.now().astimezone()
			return(now > self.startdate.astimezone())
		

	def is_past_deadline(self):
		# Return True if it is past the course deadline
		now = datetime.datetime.now().astimezone()
		return(now > self.deadline.astimezone())
		
	def is_due_soon(self):
		return(self.is_available() and not self.is_completed())
	
	
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


# User info model
class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
	if created:
		Student.objects.create(user=instance)
	instance.student.save()