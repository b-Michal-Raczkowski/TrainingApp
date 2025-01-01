from django.shortcuts import render, redirect
from .models import Workout, Category, Achievement
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
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