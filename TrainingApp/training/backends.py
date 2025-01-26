from django.contrib.auth.backends import ModelBackend, BaseBackend  # Import niestandardowych backendów uwierzytelniania
from django.contrib.auth.models import User  # Import wbudowanego modelu użytkownika Django
from django.db.models import Q  # Import klasy Q do budowania złożonych zapytań

# Backend uwierzytelniania umożliwiający logowanie za pomocą nazwy użytkownika lub adresu e-mail
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)  # Pobranie nazwy użytkownika z argumentów, jeśli brak w zmiennej
        try:
            # Wyszukiwanie użytkownika po nazwie użytkownika (case-insensitive) lub e-mailu (case-insensitive)
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            User().set_password(password)  # Zabezpieczenie przed timing attacks, ustawiając fikcyjne hasło
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                # Sprawdzenie poprawności hasła i czy użytkownik może się uwierzytelnić
                return user  # Zwrócenie użytkownika, jeśli uwierzytelnienie się powiedzie

# Niestandardowy backend uwierzytelniania
class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Wyszukiwanie użytkownika po nazwie użytkownika lub adresie e-mail
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                # Sprawdzenie poprawności hasła
                return user  # Zwrócenie użytkownika, jeśli uwierzytelnienie się powiedzie
        except User.DoesNotExist:
            return None  # Zwrócenie None, jeśli użytkownik nie istnieje

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)  # Pobranie użytkownika na podstawie jego identyfikatora
        except User.DoesNotExist:
            return None  # Zwrócenie None, jeśli użytkownik nie istnieje
