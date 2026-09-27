from django.http import HttpResponse, request
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


print("*********Django REST Framework*************")

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (PersonSerializer, DepartmentSerializer, EmployeeSerializer,
                          CreateEmployeeSerializer, PersonSerializerWithRepresentation,
                          RegisterSerializer, LoginSerializer, FoodSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Foods

@api_view(['GET'])
def api_home(request):
    return Response({"message": "Welcome to the API!"})


@api_view(['GET', 'POST'])
def api_person(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        person_serializer = PersonSerializer(persons, many=True)
        return Response({"persons": person_serializer.data})
        
    elif request.method == 'POST':
        person_serializer = PersonSerializer(data=request.data)
        if person_serializer.is_valid():
            person_serializer.save()
            return Response({"message": "Person created successfully.", "person": person_serializer.data})


@api_view(['GET', 'POST'])
def api_department(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        department_serializer = DepartmentSerializer(departments, many=True)
        return Response({"departments": department_serializer.data})
        
    elif request.method == 'POST':
        department_serializer = DepartmentSerializer(data=request.data)
        if department_serializer.is_valid():
            department_serializer.save()
            return Response({"message": "Department created successfully.", "department": department_serializer.data})

@api_view(['GET'])
def api_employee(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        employee_serializer = EmployeeSerializer(employees, many=True)
        return Response({"employees": employee_serializer.data})

@api_view(['POST'])
def api_create_employee(request):
    if request.method == 'POST':
        employee_serializer = CreateEmployeeSerializer(data=request.data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return Response({"message": "Employee created successfully.", "employee": employee_serializer.data})
        else:
            return Response({"errors": employee_serializer.errors}, status=400)

@api_view(['GET'])
def api_person_detail(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return Response({"error": "Person not found."}, status=404)

    person_serializer = PersonSerializerWithRepresentation(person)
    return Response({"person": person_serializer.data})


print("*********DRF Authentication*************")

@api_view(['POST'])
def api_register(request):
    data = request.data
    register_serializer = RegisterSerializer(data=data)
    if register_serializer.is_valid():
        register_serializer.save()
        return Response(register_serializer.data)
    return Response({"errors": register_serializer.errors}, status=400)

@api_view(['POST'])
def api_login(request):
    data = request.data
    login_serializer = LoginSerializer(data=data)
    if login_serializer.is_valid():
        username = login_serializer.validated_data['username']
        password = login_serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user) 
        return Response({"message": "Login successful.", "token": token.key})
    else:
        return Response({"error": "Invalid username or password."}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_login_details(request):
    if request.user.is_authenticated:
        return Response({"message": "User is authenticated.", "username": request.user.username})
    else:
        return Response({"message": "User is not authenticated."}, status=401)

@api_view(['GET'])
def api_food(request):
    foods = Foods.objects.filter(user=request.user)  # Filter foods by the authenticated user
    food_serializer = FoodSerializer(foods, many=True)
    return Response({"foods": food_serializer.data})

@api_view(['POST'])
def api_create_food(request):
    food_serializer = FoodSerializer(data=request.data)
    if food_serializer.is_valid():
        food_serializer.save(user=request.user)  # Associate the food with the authenticated user
        return Response({"message": "Food created successfully.", "food": food_serializer.data})
    else:
        return Response({"errors": food_serializer.errors}, status=400)


print("********* JWT Token *************")
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def jwt_login(request):
    if request.method == 'POST':
        data = request.data
        login_serializer = LoginSerializer(data=data)
        if login_serializer.is_valid():
            username = login_serializer.validated_data['username']
            password = login_serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid username or password."}, status=401)
