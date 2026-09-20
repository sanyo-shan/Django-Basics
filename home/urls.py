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
    path('seed_fake_data/', views.seed_fake_data, name='seed_fake_data'),
    path('employee/', views.employee_list, name='employee'),
    path('employee_department/<int:department_id>/', views.employee_department, name='employee_department'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home_view'),
    path('logout/', views.logout_view, name='logout'),
]
