from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, custom_logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),



]