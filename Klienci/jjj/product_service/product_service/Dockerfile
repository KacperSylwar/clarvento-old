# Wybieramy lekki obraz Pythona 3.9
FROM python:3.10-slim

# Wyłączamy zapisywanie plików .pyc oraz buforowanie logów
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy plik z zależnościami i instalujemy je
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopiujemy całą aplikację do katalogu roboczego
COPY . /app/

# Udostępniamy port 8000 (Gunicorn będzie nasłuchiwał na tym porcie)
EXPOSE 8000

# Komenda startowa – uruchamiamy Gunicorna
CMD ["gunicorn", "product_service.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]

