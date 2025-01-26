from django.urls import path  # Importuje moduł do obsługi ścieżek URL
from .views import CustomLoginView, custom_logout_view  # Importuje widoki logowania i wylogowania
from . import views  # Importuje pozostałe widoki z pliku views.py

# Definicja ścieżek URL dla aplikacji
urlpatterns = [
    path('', views.home, name='home'),  # Strona główna aplikacji
    path('profile/', views.profile, name='profile'),  # Strona profilu użytkownika
    path('register/', views.register, name='register'),  # Rejestracja nowego użytkownika
    path('login/', CustomLoginView.as_view(), name='login'),  # Logowanie użytkownika za pomocą widoku klasowego
    path('logout/', custom_logout_view, name='logout'),  # Wylogowanie użytkownika
    path('create_workout/', views.create_workout, name='create_workout'),  # Tworzenie nowego treningu
    path('your_workouts/', views.your_workouts, name='your_workouts'),  # Wyświetlanie treningów użytkownika
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),  # Usuwanie treningu utworzonego przez użytkownika
    path('new_workout/', views.select_new_workout, name='new_workout'),  # Wyświetlanie dostępnych nowych treningów
    path('add_to_your_workouts/<int:workout_id>/', views.add_to_your_workouts, name='add_to_your_workouts'),  # Dodanie treningu do listy użytkownika
    path('delete_user_workout/<int:workout_id>/', views.delete_user_workout, name='delete_user_workout'),  # Usuwanie treningu przypisanego do użytkownika
    path('edit_workout/<int:workout_id>/', views.edit_workout, name='edit_workout'),  # Edycja istniejącego treningu
    path('special_workouts/', views.special_workouts, name='special_workouts'),  # Wyświetlanie treningów specjalnych
    path('complete_special_workout/<int:workout_id>/', views.complete_special_workout, name='complete_special_workout'),  # Oznaczenie treningu specjalnego jako ukończonego
]
