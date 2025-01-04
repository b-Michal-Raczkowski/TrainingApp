from django.contrib import admin
from .models import Category, Workout, Achievement, UserProfile, UserWorkout

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration', 'created_by', 'is_admin')
    search_fields = ('title', 'difficulty')
    list_filter = ('is_admin', 'difficulty')
    filter_horizontal = ('achievement',)

admin.site.register(Category)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Achievement)
admin.site.register(UserProfile)
admin.site.register(UserWorkout)