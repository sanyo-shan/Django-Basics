from django.contrib import admin
from .models import Task, Person, Department, Employee, Skills

# Register your models here.
admin.site.register(Task)
admin.site.register(Person)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Skills)
