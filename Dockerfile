FROM python:3.13-slim

WORKDIR /app

# Zainstaluj systemowe zależności oraz narzędzia wymagane do działania MS ODBC i budowania pakietów Pythona
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    gnupg \
    ca-certificates \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dodaj klucz Microsoft i repozytorium ODBC Driver
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Skopiuj i zainstaluj zależności Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę plików projektu
COPY . .

# Zmienne środowiskowe dla Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Otwórz port
EXPOSE 5000

# Uruchom aplikację
CMD ["flask", "run", "--host=0.0.0.0"]
