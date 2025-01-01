from django.shortcuts import render, redirect
from .models import Workout, Category, Challenge, Achievement, UserWorkout, UserChallenge
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    workouts = Workout.objects.all()
    return render(request, 'training/dashboard.html', {'workouts': workouts})

@login_required
def add_workout(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        workout = Workout.objects.create(
            title=title, description=description, category=category, created_by=request.user)
        return redirect('dashboard')
    categories = Category.objects.all()
    return render(request, 'training/add_workout.html', {'categories': categories})