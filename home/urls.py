from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name = 'contact'),
    path('task/', views.task, name='task'),
    path('todo/', views.todo, name='todo'),
    path('delete_todo/<int:task_id>/', views.delete_todo, name='delete_todo'),
    path('edit_todo/<int:task_id>/', views.edit_todo, name='edit_todo'),
]
