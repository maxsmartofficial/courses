from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Course, Module, Research, Assignment, Student
from django.contrib.auth import get_user_model
# Register your models here.


class StudentInline(admin.StackedInline):
	model = Student
	can_delete = False

class UserAdmin(BaseUserAdmin):
	inlines = (StudentInline,)

class CourseAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Course, CourseAdmin)	
admin.site.register(Module)
admin.site.register(Research)
admin.site.register(Assignment)

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)