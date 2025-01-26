from django import forms  # Import modułu Django do tworzenia formularzy
from .models import User, Workout, Achievement  # Import modeli używanych w formularzach

# Formularz rejestracji użytkownika
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # Pole hasła z ukrytym wejściem (PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # Pole do potwierdzenia hasła, również ukryte

    class Meta:
        model = User  # Formularz oparty na modelu User
        fields = ('username', 'email')  # Pola, które będą widoczne w formularzu

    # Walidacja dla pola "password2" (potwierdzenie hasła)
    def clean_password2(self):
        cd = self.cleaned_data  # Pobranie oczyszczonych danych formularza
        if cd['password'] != cd['password2']:
            # Sprawdzenie, czy hasło i jego potwierdzenie są takie same
            raise forms.ValidationError('Passwords don\'t match.')
            # Rzucenie błędu walidacji, jeśli hasła się nie zgadzają
        return cd['password2']  # Zwrócenie potwierdzonego hasła, jeśli walidacja się powiedzie

# Formularz tworzenia/edycji treningu
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout  # Formularz oparty na modelu Workout
        fields = ['title', 'created_by', 'steps', 'difficulty', 'duration']
        # Pola dostępne w formularzu: tytuł, twórca, kroki, trudność i czas trwania

# Formularz tworzenia/edycji osiągnięcia
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement  # Formularz oparty na modelu Achievement
        fields = ['title', 'description']
        # Pola dostępne w formularzu: tytuł i opis osiągnięcia
