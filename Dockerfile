# Obraz bazowy
FROM python:3.13-slim

# Ustawienie zmiennych środowiskowych
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustawienie katalogu roboczego
WORKDIR /app

# Instalacja zależności Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu aplikacji
COPY . .

# Port aplikacji
EXPOSE 8000

# Uruchomienie aplikacji
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"