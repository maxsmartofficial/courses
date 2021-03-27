from django.contrib import admin
from .models import Course, Module, Research, Assignment
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Course, CourseAdmin)	
admin.site.register(Module)
admin.site.register(Research)
admin.site.register(Assignment)