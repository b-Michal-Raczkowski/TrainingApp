README

Przegląd projektu  
Ten projekt to aplikacja webowa oparta na Django do zarządzania treningami. Zawiera funkcje uwierzytelniania użytkowników, tworzenia treningów oraz ich zarządzania.  

Zawartość  

Foldery  
- `TrainingApp/`: Główny folder aplikacji.  
- `training/`: Zawiera logikę aplikacji.  
- `migrations/`: Pliki migracji bazy danych.  
- `templates/`: Szablony HTML do renderowania widoków.  
- `static/`: Pliki statyczne (CSS, JavaScript, obrazy).  

Pliki 
- `views.py`: Funkcje widoków obsługujące zapytania.  
- `models.py`: Modele bazy danych.  
- `forms.py`: Formularze do wprowadzania danych przez użytkownika.  
- `urls.py`: Trasowanie URL aplikacji.  
- `backends.py`: Niestandardowe backendy uwierzytelniania.  
- `signals.py`: Obsługa sygnałów do tworzenia profili użytkowników.  
- `apps.py`: Konfiguracja aplikacji.  
- `TrainingApp/settings.py`: Ustawienia Django dla projektu.  
- `TrainingApp/urls.py`: Trasowanie URL dla projektu.  
- `TrainingApp/wsgi.py`: Konfiguracja WSGI do wdrażania.  
- `TrainingApp/asgi.py`: Konfiguracja ASGI do wdrażania.  

Pliki  
- `manage.py`: Narzędzie wiersza poleceń Django do zadań administracyjnych.  
- `requirements.txt`: Lista zależności Pythona.  
- `README.md`: Ten plik.  

Uruchamianie aplikacji  

Wymagania wstępne 
- Python 3.x  
- Django  
- Inne zależności wymienione w `requirements.txt`  

Kroki 
1. Sklonuj repozytorium:  
   bash  
   git clone <repository_url>  
   cd TrainingApp  
   
2. Utwórz wirtualne środowisko:  
   bash  
   python -m venv venv  
   source venv/bin/activate  # Na Windows: `venv\Scripts\activate`  
   
3. Zainstaluj zależności:  
   bash  
   pip install -r requirements.txt  
   
4. Zastosuj migracje:  
   bash  
   python manage.py migrate  
   
5. Uruchom serwer deweloperski:  
   bash  
   python manage.py runserver  
   
6. Uzyskaj dostęp do aplikacji: Otwórz przeglądarkę i przejdź do [http://localhost:8000/](http://localhost:8000/).  

Dodatkowe informacje  
- Niestandardowe uwierzytelnianie: Aplikacja zawiera niestandardowe backendy uwierzytelniania zlokalizowane w `training/backends.py`.  
-Profile użytkowników: Profile użytkowników są automatycznie tworzone przy użyciu sygnałów zdefiniowanych w `training/signals.py`.  
-Szablony: Szablony HTML znajdują się w `training/templates/`.  

Szczegóły można znaleźć w komentarzach i dokumentacji w plikach kodu.  
