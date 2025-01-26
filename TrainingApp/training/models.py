from django.db.models.signals import post_save  # Import sygnału post_save, który pozwala na wykonanie określonych akcji po zapisaniu obiektu w bazie danych
from django.dispatch import receiver  # Dekorator receiver umożliwia przypisanie funkcji do sygnału
from django.db import models  # Import modeli Django
from django.contrib.auth.models import User  # Import wbudowanego modelu użytkownika Django


# Model reprezentujący osiągnięcia użytkownika
class Achievement(models.Model):
    title = models.CharField(max_length=255)  # Pole tekstowe na tytuł osiągnięcia (maks. 255 znaków)
    description = models.TextField()  # Pole tekstowe na opis osiągnięcia
    created_at = models.DateTimeField(auto_now_add=True)  # Automatyczne ustawienie daty i czasu utworzenia

    def __str__(self):
        return self.title  # Reprezentacja tekstowa osiągnięcia

# Model reprezentujący treningi
class Workout(models.Model):
    title = models.CharField(max_length=255)  # Pole tekstowe na tytuł treningu
    difficulty = models.CharField(max_length=50)  # Pole tekstowe na poziom trudności
    duration = models.IntegerField()  # Pole liczbowe na czas trwania treningu (w minutach)
    steps = models.TextField()  # Pole tekstowe na kroki/etapy treningu
    is_admin = models.BooleanField(default=False)  # Pole logiczne wskazujące, czy trening został stworzony przez administratora
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Pole powiązane z użytkownikiem, który stworzył trening. Usunięcie użytkownika powoduje usunięcie powiązanych treningów.
    created_at = models.DateTimeField(auto_now_add=True)  # Automatyczne ustawienie daty i czasu utworzenia
    achievement = models.ForeignKey(Achievement, on_delete=models.SET_NULL, null=True, blank=True)
    # Pole powiązane z osiągnięciem, które można uzyskać za ten trening. Usunięcie osiągnięcia ustawia wartość NULL.

    def __str__(self):
        return self.title  # Reprezentacja tekstowa treningu

# Model powiązania użytkowników z treningami
class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Powiązanie z użytkownikiem
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Powiązanie z treningiem
    added_at = models.DateTimeField(auto_now_add=True)  # Data i czas dodania treningu do użytkownika
    achievements = models.ManyToManyField(Achievement, blank=True)
    # Lista osiągnięć powiązanych z użytkownikiem w kontekście danego treningu

    def __str__(self):
        return f"{self.user.username} - {self.workout.title}"  # Reprezentacja tekstowa w formacie: "użytkownik - trening"

# Model profilu użytkownika
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Jeden profil przypisany do jednego użytkownika
    photo = models.ImageField(upload_to='profile_photos', default='default.jpg')
    # Pole do przechowywania zdjęcia profilowego użytkownika
    achievements = models.ManyToManyField(Achievement, blank=True)
    # Lista osiągnięć przypisanych do użytkownika

    def __str__(self):
        return self.user.username  # Reprezentacja tekstowa w postaci nazwy użytkownika

# Sygnał tworzący profil użytkownika po utworzeniu nowego użytkownika
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Jeśli użytkownik został stworzony...
        UserProfile.objects.create(user=instance)  # Tworzy nowy profil użytkownika

# Sygnał zapisujący zmiany w profilu użytkownika po zapisaniu użytkownika
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # Zapisuje zmiany w profilu użytkownika
