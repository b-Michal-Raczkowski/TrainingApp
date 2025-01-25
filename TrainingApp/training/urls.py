from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('create_workout/', views.create_workout, name='create_workout'),
    path('your_workouts/', views.your_workouts, name='your_workouts'),
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('select_new_workout/', views.select_new_workout, name='select_new_workout'),
    path('add_to_your_workouts/<int:workout_id>/', views.add_to_your_workouts, name='add_to_your_workouts'),
    path('delete_user_workout/<int:workout_id>/', views.delete_user_workout, name='delete_user_workout'),
    path('edit_workout/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('special_workouts/', views.special_workouts, name='special_workouts'),
    path('complete_special_workout/<int:workout_id>/', views.complete_special_workout, name='complete_special_workout'),


]