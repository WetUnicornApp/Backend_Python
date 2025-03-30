# Użyj obrazu z Pythonem 3.13 jako bazowego
FROM python:3.13-slim

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Kopiowanie pliku requirements.txt do kontenera
COPY requirements.txt .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu aplikacji do kontenera
COPY .. .

# Ustawienie zmiennej środowiskowej w kontenerze
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Otworzenie portu, na którym aplikacja będzie działać
EXPOSE 5000

# Uruchomienie aplikacji Flask
CMD ["flask", "run", "--host=0.0.0.0"]
