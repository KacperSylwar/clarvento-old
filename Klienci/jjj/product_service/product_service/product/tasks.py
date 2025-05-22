# product/tasks.py
import csv
import io
import os
import requests
from urllib.parse import urlparse

from django.utils.text import slugify
from django.core.files.base import ContentFile
from celery import shared_task

from .models import Manufacturer, ProductCategory, Product, ProductImage


@shared_task
def process_csv_file(file_data):
    """
    Zadanie asynchroniczne, które przetwarza zawartość pliku CSV,
    pobiera obrazy i tworzy obiekty Manufacturer, ProductCategory, Product oraz ProductImage.
    """
    # Usuń BOM, jeśli występuje
    file_data = file_data.replace('\ufeff', '')
    io_string = io.StringIO(file_data)

    # Używamy średnika jako delimiter, ponieważ dane są rozdzielane średnikami
    csv_reader = csv.DictReader(io_string, delimiter=';')

    # Debug: wypisanie kluczy pierwszego wiersza CSV
    try:
        first_row = next(csv_reader)
        print("Klucze w pierwszym wierszu CSV:", list(first_row.keys()))
        # Resetujemy wskaźnik, aby przetworzyć cały plik od początku
        io_string.seek(0)
        csv_reader = csv.DictReader(io_string, delimiter=';')
    except StopIteration:
        print("CSV jest pusty!")
        return "Przetworzono 0 rekordów z pliku CSV."

    count = 0

    for row in csv_reader:
        # Pobieramy dane – upewnij się, że nagłówki w CSV odpowiadają poniższym nazwom
        product_name = row.get("Product Name", "").strip()
        kategoria = row.get("Kategoria", "").strip()
        producent = row.get("Producent", "").strip()
        detail_name = row.get("Detail Name", "").strip()
        description = row.get("Description", "").strip()
        images_field = row.get("Images", "").strip()

        # Debug: wypisanie wiersza, żeby sprawdzić dane
        print("Odczytany wiersz:", row)

        # Pomijamy wiersze bez nazwy produktu
        if not product_name:
            print("Pominięto wiersz, brak 'Product Name'")
            continue

        # Tworzymy lub pobieramy producenta
        manufacturer_obj, _ = Manufacturer.objects.get_or_create(
            name=producent,

        )

        # Tworzymy lub pobieramy kategorię
        category_obj, _ = ProductCategory.objects.get_or_create(
            name=kategoria,

        )

        # Tworzymy nowy produkt
        product_obj = Product.objects.create(
            name=product_name,
            description=description,
            application=detail_name,
            manufacturer=manufacturer_obj,
            slug=slugify(product_name)[:255]
        )
        product_obj.categories.add(category_obj)

        # Pobieranie i zapisywanie obrazów, jeśli są podane
        if images_field:
            images_list = [img.strip() for img in images_field.split(';') if img.strip()]
            for image_url in images_list:
                try:
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        parsed_url = urlparse(image_url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename:
                            filename = f"image_{product_obj.id}.jpg"
                        product_image = ProductImage(product=product_obj)
                        product_image.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                    else:
                        print(f"[WARN] Nie udało się pobrać obrazu: {image_url} (status: {response.status_code})")
                except Exception as e:
                    print(f"[ERROR] Błąd pobierania obrazu {image_url}: {e}")

        count += 1

    return f"Przetworzono {count} rekordów z pliku CSV."
