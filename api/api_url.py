from django.urls import path
from home import views

urlpatterns = [
    path('home/', views.api_home, name='home'),
    path('person/', views.api_person, name='person'),
    path('employee/', views.api_employee, name='employee'),
    path('department/', views.api_department, name='department'),
    path('create-employee/', views.api_create_employee, name='create-employee'),
    path('person/<int:person_id>/', views.api_person_detail, name='person-detail'),
    path('register/', views.api_register, name='register'),
    path('login/', views.api_login, name='login'),
    path('login-detail/', views.api_login_details, name='login-detail'),
    path('food/', views.api_food, name='food'),
    path('create-food/', views.api_create_food, name='create-food'),
    path('jwt-login/', views.jwt_login, name='jwt-login'),
]