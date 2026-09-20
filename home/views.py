from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Task, Person, Department, Employee
from faker import Faker
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')
    return HttpResponse("Hello, welcome to the home page!")

def index(request):
    #return HttpResponse("Index Page")
    fruits = ['Apple', 'Banana', 'Cherry', 'Guava', 'Berry']

    return render(request, 'index.html', context= {'fruits': fruits})

def contact(request):
    contacts = [{
        'name': 'John Doe', 'age': 30, 'profession': 'Engineer'
    }, {
        'name': 'Jane Smith', 'age': 25, 'profession': 'Designer'
    }, {
        'name': 'Bob Johnson', 'age': 35, 'profession': 'Manager'
    }]

    return render(request, 'contact.html', context={'contacts': contacts})

def task(request):
    tasks = [
        {'title': 'Study Django', 'completed': True},
        {'title': 'Build a Todo App', 'completed': False},
        {'title': 'Deploy the App', 'completed': True},
        {'title': 'Write Documentation', 'completed': False},
    ]

    for task in tasks:
        t = Task(title=task['title'], completed=task['completed'])
        t.save()
        print(f"Task '{t.title}' saved to the database.")

    return render(request, 'task.html', context={'tasks': tasks})
    
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponse("Task not found.", status=404)

    return render(request, 'task.html', context={'task': task})

def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        completed = request.POST.get('completed') == 'on'
        task = Task(title=title, completed=completed)
        task.save()
        return redirect('todo')  # Redirect to the same page after saving the task

    tasks = Task.objects.all()
    return render(request, 'todo.html', context={'tasks': tasks})

def delete_todo(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('todo')  # Redirect to the todo page after deletion
    except Task.DoesNotExist:
        return HttpResponse("Task not found.", status=404)

def edit_todo(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponse("Task not found.", status=404)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('todo')  # Redirect to the todo page after editing the task

    return render(request, 'todo.html', context={'task': task})


def seed_fake_data(request):
    fake = Faker()

    for _ in range(50):  # Generate 50 fake persons
        Department.objects.create(name=fake.company())

    for _ in range(50):  # Generate 50 fake tasks
        departments = Department.objects.all()
        Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email(),
            age=fake.random_int(min=18, max=65),
            salary=fake.random_number(digits=5),
            city=fake.city(),
            joining_date=fake.date_this_decade(),
            is_active=fake.boolean(),
            department=random.choice(Department.objects.all())  # Assign a random department
        )

    return HttpResponse("Fake data seeded successfully.")

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', context={'employees': employees})

def employee_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return HttpResponse("Department not found.", status=404)

    employees = Employee.objects.filter(department=department)
    return render(request, 'employee_list.html', context={'department': department, 'employees': employees})

def employee_detail(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)

    return render(request, 'employee_detail.html', context={'employee': employee})

@csrf_exempt
def register(request):
    # messages.info(request, "Registering a new user.")
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')

        print(f"Received registration data: username={username}, firstname={firstname}, lastname={lastname}")

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists. Please choose a different username.")
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
        #user.set_password(password)  # Hash the password
        user.save()
        messages.success(request, "User registered successfully.")

    return render(request, 'registration.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print(request.user.is_authenticated)  # Check if the user is authenticated before login

        login(request, user)  # Log the user in if authentication is successful

        if user is not None:
            print(request.user.is_authenticated)
            return redirect('home_view')  # Redirect to the home view after successful login
        else:
            return HttpResponse("Invalid username or password!")

@login_required
def home_view(request):
    return render(request, 'home.html',
                context={'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('register')  # Redirect to the registration page after logout