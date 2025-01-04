# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from .models import Workout, Achievement, UserWorkout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import UserRegistrationForm, WorkoutForm, SpecialWorkoutForm
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .utils import award_achievement
import re
import json

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        return super().post(request, *args, **kwargs)

@login_required
def add_to_your_workouts(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    user_workout, created = UserWorkout.objects.get_or_create(user=request.user, workout=workout)
    if not created:
        return JsonResponse({'success': False, 'error': 'Workout already added to your workouts'}, status=400)

    # Ensure the workout is marked as a community workout
    workout.is_admin = True
    workout.save()

    return JsonResponse({'success': True})

@require_http_methods(["DELETE"])
@login_required
def delete_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)
        # Delete related UserWorkout entries
        UserWorkout.objects.filter(workout=workout).delete()
        # Delete the workout itself
        workout.delete()
        return JsonResponse({'success': True})
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found or not created by user'}, status=404)

@login_required
@require_http_methods(["DELETE"])
def delete_user_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)
        workout.delete()
        return JsonResponse({'success': True})
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found'})

@method_decorator(csrf_exempt, name='dispatch')
def register(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = UserRegistrationForm()
    return render(request, 'training/register.html', {'form': form})

def home(request):
    return render(request, 'training/home.html')

def custom_logout_view(request):
    logout(request)
    return redirect('home')


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_workout(request):
    if not request.body:
        return JsonResponse({'success': False, 'error': 'Empty request body'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    steps = data.pop('steps', [])
    data['steps'] = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(steps))
    data['created_by'] = request.user.id  # Set the created_by field
    form = WorkoutForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': form.errors.as_json()})

@login_required
def select_new_workout(request):
    user_workouts = Workout.objects.filter(
        is_admin=False,
        created_by__isnull=False,
        created_by__is_active=True
    ).exclude(
        id__in=UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True)
    )
    admin_workouts = Workout.objects.filter(
        is_admin=True,
        created_by__isnull=True
    )
    special_workouts = Workout.objects.filter(is_admin=True)
    user_workout_ids = UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True)
    context = {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
        'special_workouts': special_workouts,
        'user_workout_ids': user_workout_ids,
    }
    return render(request, 'training/select_new_workout.html', context)

@login_required
def your_workouts(request):
    user_workouts = Workout.objects.filter(created_by=request.user, is_admin=False)
    admin_workouts = Workout.objects.filter(is_admin=True, userworkout__user=request.user)
    return render(request, 'training/your_workouts.html', {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
    })

@login_required
def achievements_view(request):
    user_achievements = Achievement.objects.filter(user=request.user)
    uncollected_achievements = Achievement.objects.exclude(user=request.user)

    context = {
        'user_achievements': user_achievements,
        'uncollected_achievements': uncollected_achievements,
    }
    return render(request, 'training/achievements.html', context)
@login_required
def profile(request):
    achievements_count = Achievement.objects.filter(user=request.user).count()
    return render(request, 'training/profile.html', {
        'achievements_count': achievements_count
    })
@csrf_exempt
@require_http_methods(["PUT"])
@login_required
def edit_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    steps = data.get('steps', workout.steps.split('\n'))

    # Remove existing numbering if present
    def remove_numbering(step):
        return re.sub(r"^\d+\.\s*", "", step)  # Removes "1. ", "2. ", etc., at the start of a step

    clean_steps = [remove_numbering(step) for step in steps]

    # Re-number steps
    data['steps'] = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(clean_steps))

    # Preserve existing fields not in the request
    data['title'] = data.get('title', workout.title)
    data['difficulty'] = data.get('difficulty', workout.difficulty)
    data['duration'] = data.get('duration', workout.duration)
    data['is_admin'] = workout.is_admin
    data['created_by'] = workout.created_by.id

    form = WorkoutForm(data, instance=workout)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': form.errors.as_json()})



def special_workouts(request):
    special_workouts = Workout.objects.filter(is_admin=True)
    return render(request, 'training/special_workouts.html', {'special_workouts': special_workouts})
@staff_member_required
@require_POST
def post_achievement(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    title = request.POST.get('title')
    description = request.POST.get('description')

    if not title or not description:
        return JsonResponse({'success': False, 'error': 'Title and description are required'}, status=400)

    award_achievement(workout, title, description)
    return JsonResponse({'success': True})


@require_POST
@login_required
def complete_special_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, is_admin=True)
    user_workout = UserWorkout.objects.filter(user=request.user, workout=workout).first()

    if user_workout:
        user_workout.delete()
        award_achievement(request.user, f"Completed {workout.title}",
                          f"Awarded for completing the special workout: {workout.title}")
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Workout not found in your list'})

@login_required
def your_achievements(request):
    collected_achievements = Achievement.objects.filter(user=request.user, collected=True)
    uncollected_achievements = Achievement.objects.filter(user=request.user, collected=False)
    return render(request, 'training/achievements.html', {
        'collected_achievements': collected_achievements,
        'uncollected_achievements': uncollected_achievements
    })

