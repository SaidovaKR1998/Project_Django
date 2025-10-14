from django.urls import path
from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]