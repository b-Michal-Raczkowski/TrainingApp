from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_workout/', views.add_workout, name='add_workout'),
]