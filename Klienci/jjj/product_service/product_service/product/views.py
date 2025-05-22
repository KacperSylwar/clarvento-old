from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer
from .models import (
    Product,ProductCategory,Manufacturer
)
from django.core.paginator import Paginator
from rest_framework.exceptions import NotFound
from .serializers import  (ProductSerializer,AllProductsSerializer, CategorySerializer, AllCategorySerializer,
                           CategoryWithProductCountSerializer, ManufacturerWithProductCountSerializer,HomeProductsSerializer,AllManufacturerSerializer,
                           ManufacturerSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination

class ManufacturerDetailView(generics.RetrieveAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def get_object(self):
        slug = self.kwargs.get('slug')
        manufacturer = Manufacturer.objects.prefetch_related('products__images').filter(slug=slug).first()
        if not manufacturer:
            raise NotFound('Manufacturer not found')
        return manufacturer

    def get_serializer_context(self):
        return {'request': self.request}


class ManufacturerListView(generics.ListAPIView):
    """
    Widok zwracający listę wszystkich producentów.
    """
    serializer_class = AllManufacturerSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    search_fields = ['name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Domyślny sposób sortowania

    def get_queryset(self):
        return Manufacturer.objects.all()

    def get_serializer_context(self):
        lang = self.kwargs.get('lang', 'pl')
        return {
            'lang': lang,
            'request': self.request
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        return Response(data)


class CategoryWithProductCountView(generics.ListAPIView):
    serializer_class = CategoryWithProductCountSerializer
    renderer_classes = [JSONRenderer]  # ✅ Ustawienie JSONRenderer

    def get_queryset(self):
        return ProductCategory.objects.annotate(product_count=Count('products'))

class ManufacturerWithProductCountView(generics.ListAPIView):
    serializer_class = ManufacturerWithProductCountSerializer
    renderer_classes = [JSONRenderer]  # ✅ Ustawienie JSONRenderer

    def get_queryset(self):
        return Manufacturer.objects.annotate(product_count=Count('products'))


class CustomPagination2(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomPagination(PageNumberPagination):
        page_size = 15
        page_size_query_param = 'page_size'
        max_page_size = 100


class CategoryDetailView(generics.RetrieveAPIView):  # ✅ Wracamy do RetrieveAPIView
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def get_object(self):
        slug = self.kwargs.get('slug')
        category = ProductCategory.objects.prefetch_related('products__images').filter(slug=slug).first()
        if not category:
            from rest_framework.exceptions import NotFound
            raise NotFound('Category not found')
        return category

    def get_serializer_context(self):
        request = self.request
        return {'request': request}


class CategoryListView(generics.ListAPIView):
    """
    Widok zwracający listę wszystkich kategorii.
    """
    serializer_class = AllCategorySerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    search_fields = ['name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Domyślny sposób sortowania

    def get_queryset(self):
        return ProductCategory.objects.all()

    def get_serializer_context(self):
        lang = self.kwargs.get('lang', 'pl')
        return {
            'lang': lang,
            'request': self.request
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        return Response(data)

class ProductListView(generics.ListAPIView):
    """
    Widok zwracający listę wszystkich produktów.
    """
    serializer_class = AllProductsSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    search_fields = ['name', 'description', 'categories__name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Domyślny sposób sortowania

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_context(self):
        lang = self.kwargs.get('lang', 'pl')
        return {
            'lang': lang,
            'request': self.request
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data


        return Response(data)

class ProductDetailViewBySlug(generics.RetrieveAPIView):
    """
    Widok zwracający szczegóły produktu na podstawie jego slug-a.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_context(self):
        lang = self.kwargs.get('lang', 'pl')  # Pobierz język z URL
        return {'lang': lang,
                'request': self.request}

from .tasks import process_csv_file

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response(
                {"error": "Nie znaleziono pliku w żądaniu. Upewnij się, że pole nazywa się 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES['file']

        if not file_obj.name.endswith('.csv'):
            return Response(
                {"error": "Plik musi mieć rozszerzenie .csv"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Odczytujemy zawartość pliku
        file_data = file_obj.read().decode('utf-8', errors='replace')

        # Wywołujemy zadanie asynchroniczne
        task = process_csv_file.delay(file_data)
        return Response(
            {"message": "Import został uruchomiony. Zadanie ID: " + task.id},
            status=status.HTTP_202_ACCEPTED
        )


class ProductHomepageView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        # Pobierz wszystkie produkty, możesz dodać filtr, np. show_on_homepage=True
        products = Product.objects.all().order_by('-created_at')
        # Pobieramy parametry paginacji z query string lub ustawiamy wartości domyślne
        page_size = int(request.query_params.get('page_size', 30))
        page = int(request.query_params.get('page', 1))
        paginator = Paginator(products, page_size)

        try:
            products_page = paginator.page(page)
        except Exception:
            # Jeśli numer strony jest niepoprawny, pobieramy pierwszą stronę
            products_page = paginator.page(1)

        serializer = ProductSerializer(products_page, many=True, context={'request': request})
        return Response({
            'count': paginator.count,
            'next': products_page.next_page_number() if products_page.has_next() else None,
            'previous': products_page.previous_page_number() if products_page.has_previous() else None,
            'results': serializer.data
        })