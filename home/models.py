from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Person: {self.name}, Age: {self.age}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Department: {self.name}"

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE) 

class Skills(models.Model):
    name = models.CharField(max_length=100)
    employee = models.ManyToManyField(Employee, related_name='skills')