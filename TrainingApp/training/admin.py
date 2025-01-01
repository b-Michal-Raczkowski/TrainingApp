from django.contrib import admin
from .models import Category, Workout, Challenge, Achievement, UserProfile, UserWorkout, UserChallenge

admin.site.register(Category)
admin.site.register(Workout)
admin.site.register(Challenge)
admin.site.register(Achievement)
admin.site.register(UserProfile)
admin.site.register(UserWorkout)
admin.site.register(UserChallenge)