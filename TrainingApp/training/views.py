from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from .models import Workout, UserWorkout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import UserRegistrationForm, WorkoutForm
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
import json

class CustomLoginView(LoginView):
    template_name = 'base.html'  # Ścieżka do szablonu dla strony logowania

    # Obsługuje żądania GET do logowania
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Sprawdza, czy żądanie jest AJAX
            return JsonResponse({'error': 'GET method not allowed'}, status=405)
        return HttpResponse(status=405)

    # Obsługuje żądania POST do logowania użytkownika
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Obsługuje żądania AJAX
            username = request.POST.get('username')  # Pobiera nazwę użytkownika
            password = request.POST.get('password')  # Pobiera hasło
            user = authenticate(request, username=username, password=password)  # Próba uwierzytelnienia
            if user is not None:
                login(request, user)  # Loguje użytkownika
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Dodaje trening do listy użytkownika
@login_required
def add_to_your_workouts(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)  # Pobiera obiekt treningu lub zgłasza 404
    user_workout, created = UserWorkout.objects.get_or_create(user=request.user, workout=workout)  # Dodaje trening do użytkownika
    if not created:
        return JsonResponse({'success': False, 'error': 'Workout already added to your workouts'}, status=400)

    workout.is_admin = True  # Oznacza trening jako społecznościowy
    workout.save()

    return JsonResponse({'success': True})

# Usuwa trening utworzony przez użytkownika
@require_http_methods(["DELETE"])
@login_required
def delete_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)  # Sprawdza, czy trening należy do użytkownika
        UserWorkout.objects.filter(workout=workout).delete()  # Usuwa powiązane wpisy UserWorkout
        workout.delete()  # Usuwa sam trening
        return JsonResponse({'success': True})
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found or not created by user'}, status=404)

# Usuwa trening przypisany do użytkownika
@login_required
@require_http_methods(["DELETE"])
def delete_user_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)  # Sprawdza, czy trening istnieje
        workout.delete()
        return JsonResponse({'success': True})
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found'})

# Rejestruje nowego użytkownika
@method_decorator(csrf_exempt, name='dispatch')
def register(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Obsługuje AJAX POST
        form = UserRegistrationForm(request.POST)  # Tworzy formularz rejestracji
        if form.is_valid():
            new_user = form.save(commit=False)  # Tworzy nowego użytkownika, ale nie zapisuje go jeszcze
            new_user.set_password(form.cleaned_data['password'])  # Ustawia hasło
            new_user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = UserRegistrationForm()  # Jeśli nie POST, zwraca pusty formularz
    return render(request, 'training/register.html', {'form': form})

# Wyświetla stronę główną
def home(request):
    return render(request, 'training/home.html')

# Wylogowuje użytkownika
def custom_logout_view(request):
    logout(request)  # Wylogowuje użytkownika
    return redirect('home')

# Tworzy nowy trening
@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_workout(request):
    if not request.body:
        return JsonResponse({'success': False, 'error': 'Empty request body'}, status=400)

    try:
        data = json.loads(request.body)  # Parsuje JSON
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    steps = data.pop('steps', [])  # Pobiera kroki treningu
    data['steps'] = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(steps))  # Dodaje numerację do kroków
    data['created_by'] = request.user.id  # Ustawia autora
    form = WorkoutForm(data)  # Tworzy formularz treningu
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': form.errors.as_json()})

# Wyświetla dostępne nowe treningi
@login_required
def select_new_workout(request):
    user_workouts = Workout.objects.filter(
        is_admin=False,  # Filtruje treningi niebędące administracyjnymi
        created_by__isnull=False,  # Wyklucza treningi bez przypisanego twórcy
        created_by__is_active=True  # Uwzględnia tylko aktywnych użytkowników
    ).exclude(
        id__in=UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True)  # Wyklucza treningi już dodane do użytkownika
    )
    admin_workouts = Workout.objects.filter(
        is_admin=True,  # Filtruje treningi administracyjne
        created_by__isnull=True  # Uwzględnia tylko treningi bez twórcy (globalne)
    )
    special_workouts = Workout.objects.filter(is_admin=True)  # Pobiera wszystkie treningi administracyjne
    user_workout_ids = UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True)  # Pobiera ID treningów użytkownika
    context = {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
        'special_workouts': special_workouts,
        'user_workout_ids': user_workout_ids,
    }
    return render(request, 'training/select_new_workout.html', context)  # Renderuje stronę z nowymi treningami

# Wyświetla treningi użytkownika
@login_required
def your_workouts(request):
    user_workouts = Workout.objects.filter(created_by=request.user, is_admin=False)  # Pobiera treningi stworzone przez użytkownika
    admin_workouts = Workout.objects.filter(is_admin=True, userworkout__user=request.user)  # Pobiera treningi administracyjne przypisane do użytkownika
    return render(request, 'training/your_workouts.html', {
        'user_workouts': user_workouts,
        'admin_workouts': admin_workouts,
    })

# Wyświetla profil użytkownika
@login_required
def profile(request):
    return render(request, 'training/profile.html', {})  # Renderuje stronę profilu użytkownika

# Edytuje istniejący trening
@csrf_exempt
@require_http_methods(["PUT"])
@login_required
def edit_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id, created_by=request.user)  # Sprawdza, czy trening należy do użytkownika
    except Workout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Workout not found'}, status=404)

    try:
        data = json.loads(request.body)  # Parsuje dane JSON
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    steps = data.get('steps', workout.steps.split('\n'))  # Pobiera kroki lub używa istniejących

    def remove_numbering(step):
        return re.sub(r"^\d+\.\s*", "", step)  # Usuwa numerację z kroków

    clean_steps = [remove_numbering(step) for step in steps]  # Czyści kroki z numeracji

    data['steps'] = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(clean_steps))  # Dodaje nową numerację do kroków
    data['title'] = data.get('title', workout.title)  # Aktualizuje tytuł
    data['difficulty'] = data.get('difficulty', workout.difficulty)  # Aktualizuje poziom trudności
    data['duration'] = data.get('duration', workout.duration)  # Aktualizuje czas trwania
    data['is_admin'] = workout.is_admin  # Zachowuje status administracyjny
    data['created_by'] = workout.created_by.id  # Zachowuje twórcę treningu

    form = WorkoutForm(data, instance=workout)  # Tworzy formularz edycji
    if form.is_valid():
        form.save()  # Zapisuje zmiany
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': form.errors.as_json()})

# Wyświetla treningi specjalne
@login_required
def special_workouts(request):
    special_workouts = Workout.objects.filter(is_admin=True)  # Pobiera treningi specjalne (administracyjne)
    return render(request, 'training/special_workouts.html', {'special_workouts': special_workouts})

# Oznacza trening specjalny jako ukończony
@require_POST
@login_required
def complete_special_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, is_admin=True)  # Pobiera trening administracyjny lub zgłasza 404
    user_workout = UserWorkout.objects.filter(user=request.user, workout=workout).first()  # Sprawdza, czy trening jest przypisany do użytkownika

    if user_workout:
        user_workout.delete()  # Usuwa powiązanie treningu z użytkownikiem
        if workout.achievement:  # Jeśli trening ma przypisane osiągnięcie
            request.user.profile.achievements.add(workout.achievement)  # Dodaje osiągnięcie do profilu użytkownika
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Workout not found in your list'})
