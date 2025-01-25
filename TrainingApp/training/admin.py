from django.contrib import admin
from .models import Workout, UserProfile, UserWorkout

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration', 'created_by', 'is_admin')
    search_fields = ('title', 'difficulty')
    list_filter = ('is_admin', 'difficulty')



admin.site.register(Workout, WorkoutAdmin)
admin.site.register(UserProfile)
admin.site.register(UserWorkout)