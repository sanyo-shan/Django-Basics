from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Task

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

