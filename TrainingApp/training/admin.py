from django.contrib import admin  # Import modułu administracyjnego Django
from .models import Workout, UserProfile, UserWorkout, Achievement  # Import modeli aplikacji

# Klasa konfiguracyjna dla modelu Workout w panelu administracyjnym
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration', 'created_by', 'is_admin')
    # Kolumny wyświetlane w liście obiektów w panelu admina
    search_fields = ('title', 'difficulty')
    # Pola, które można przeszukiwać w panelu administracyjnym
    list_filter = ('is_admin', 'difficulty')
    # Filtry umożliwiające sortowanie według wskazanych pól

# Klasa konfiguracyjna dla modelu Achievement w panelu administracyjnym
@admin.register(Achievement)  # Dekorator rejestrujący model Achievement w panelu admina
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    # Kolumny wyświetlane w liście obiektów w panelu admina
    search_fields = ('title', 'description')
    # Pola, które można przeszukiwać w panelu administracyjnym

# Rejestracja modeli w panelu administracyjnym
admin.site.register(Workout, WorkoutAdmin)  # Rejestracja modelu Workout z niestandardową konfiguracją
admin.site.register(UserProfile)  # Rejestracja modelu UserProfile z domyślnymi ustawieniami
admin.site.register(UserWorkout)  # Rejestracja modelu UserWorkout z domyślnymi ustawieniami
