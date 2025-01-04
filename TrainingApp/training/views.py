from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Workout, Achievement, UserWorkout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import UserRegistrationForm, WorkoutForm
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
@require_http_methods(["DELETE"])
@login_required
def delete_user_workout(request, workout_id):
    try:
        user_workout = UserWorkout.objects.get(user=request.user, workout_id=workout_id)
        user_workout.delete()
        return JsonResponse({'success': True})
    except UserWorkout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found in your workouts'}, status=404)

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

@login_required
def profile(request):
    user = request.user
    achievements_count = Achievement.objects.filter(user=user).count()
    return render(request, 'training/profile.html', {
        'user': user,
        'achievements_count': achievements_count
    })

def home(request):
    return render(request, 'training/home.html')

def custom_logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    workouts = Workout.objects.all()
    return render(request, 'training/dashboard.html', {'workouts': workouts})


@login_required
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.created_by = request.user
            workout.save()
            return redirect('your_workouts')
    else:
        form = WorkoutForm()
    return render(request, 'training/create_workout.html', {'form': form})

@login_required
def select_new_workout(request):
    user_workouts = Workout.objects.filter(
        is_admin=False,
        created_by__isnull=False,
        created_by__is_active=True
    ).exclude(
        id__in=UserWorkout.objects.filter(user=request.user, deleted=True).values_list('workout_id', flat=True)
    )
    admin_workouts = Workout.objects.filter(
        is_admin=True,
        created_by__isnull=True
    )
    user_workout_ids = UserWorkout.objects.filter(user=request.user, deleted=False).values_list('workout_id', flat=True)
    context = {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
        'user_workout_ids': user_workout_ids,
    }
    return render(request, 'training/select_new_workout.html', context)

@login_required
def your_workouts(request):
    user_workouts = Workout.objects.filter(userworkout__user=request.user, is_admin=False)
    admin_workouts = Workout.objects.filter(is_admin=True, userworkout__user=request.user)
    return render(request, 'training/your_workouts.html', {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
    })