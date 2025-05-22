from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.utils.text import slugify
import os


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nazwa producenta")
    description = models.TextField(verbose_name="Opis producenta", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", blank=True)

    class Meta:
        verbose_name = "Producent"
        verbose_name_plural = "Producenci"
        ordering = ["-name"]

    def __str__(self):
        return self.name




class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nazwa kategorii")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", blank=True, null=True)
    description = models.TextField(verbose_name="Opis kategorii", blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )

    class Meta:
        verbose_name = "Kategoria produktów"
        verbose_name_plural = "Kategorie produktów"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    # Podstawowe informacje o produkcie
    name = models.CharField(max_length=255, verbose_name="Nazwa produktu", default="Nazwa produktu")
    description = models.TextField(verbose_name="Opis produktu", default="Opis produktu")
    application = models.TextField(verbose_name="Zastosowanie", blank=True, null=True)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    categories = models.ManyToManyField(ProductCategory, related_name='products', verbose_name='Kategorie')

    # Dane techniczne
    power = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Moc (W)", blank=True, null=True)
    dimensions = models.CharField(max_length=50, verbose_name="Wymiary (cm)", blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Waga (kg)", blank=True, null=True)
    operating_temperature = models.CharField(max_length=50, verbose_name="Temperatura pracy", blank=True, null=True)
    protection_class = models.CharField(max_length=20, verbose_name="Klasa ochrony", blank=True, null=True)
    power_tolerance = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Tolerancja mocy (%)", blank=True, null=True)

    # Ceny
    price_net_no_markup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena netto bez marży", blank=True, null=True)
    price_gross_no_markup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena brutto bez marży", blank=True, null=True)
    price_net_with_markup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena netto z marżą", blank=True, null=True)
    price_gross_with_markup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena brutto z marżą", blank=True, null=True)

    # Informacje o producencie i dokumentacji
    country_of_origin = models.CharField(max_length=100, verbose_name="Kraj pochodzenia", blank=True, null=True)
    warranty_period = models.CharField(max_length=50, verbose_name="Okres gwarancji", blank=True, null=True)

    # Dodatkowe informacje
    advantages = models.TextField(verbose_name="Funkcje i zalety", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Stan magazynowy
    stock = models.PositiveIntegerField(verbose_name="Stan magazynowy", default=0, blank=True, null=True)
    out_of_stock = models.BooleanField(verbose_name="Brak w magazynie", default=False)

    # SEO
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", blank=True)
    meta_title = models.CharField(max_length=255, verbose_name="Meta Title", blank=True, null=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True, null=True)
    structured_data = models.JSONField(verbose_name="Structured Data", blank=True, null=True)

    # Sponsorowane
    show_on_homepage = models.BooleanField(verbose_name="Show on Homepage", default=False)
    is_promotion = models.BooleanField(verbose_name="Promotion", default=False)
    is_sponsored = models.BooleanField(verbose_name="Sponsored", default=False)

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"
        ordering = ["-name"]

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products", verbose_name="Zdjęcie produktu")

    class Meta:
        verbose_name = "Zdjęcie produktu"
        verbose_name_plural = "Zdjęcia produktów"
        ordering = ["-product"]

    def __str__(self):
        return self.product.name


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="products", verbose_name="Plik")

    class Meta:
        verbose_name = "Plik produktu"
        verbose_name_plural = "Pliki produktów"
        ordering = ["-product"]

    def __str__(self):
        return self.product.name
