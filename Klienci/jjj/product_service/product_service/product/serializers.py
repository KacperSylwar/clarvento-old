from rest_framework import serializers
from .models import (
    Product, ProductImage, ProductCategory, Manufacturer
)
from django.core.paginator import Paginator

#############################################################################################################
# Serializery do obsługi API Produkty
#############################################################################################################

#Serializer do wyświetlania zdjęć produktów
class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        print(f"Request: {request}")  # Sprawdź, czy request istnieje
        print(f"Image path: {obj.image.url}")  # Sprawdź, czy istnieje ścieżka do zdjęcia

        if obj.image:
            image_url = request.build_absolute_uri(obj.image.url) if request else obj.image.url
            print(f"Image URL: {image_url}")  # Debug URL
            return image_url
        return None

#Serializer do wyświetlania wszystkich produktów
class AllProductsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['name','slug']

    def get_name(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'name_{lang}', obj.name)

# Serializer do wyświetlania produktów na stronie głównej
class HomeProductsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product']

    def get_product(self, obj):
        request = self.context.get('request')
        page_size = int(request.query_params.get('page_size', 15))
        page = int(request.query_params.get('page', 1))

        # Obsługa paginacji
        products = obj.products.all()
        paginator = Paginator(products, page_size)

        try:
            products_page = paginator.page(page)
        except Exception:
            products_page = []

        return {
            'count': paginator.count,
            'next': products_page.next_page_number() if products_page and hasattr(products_page, 'has_next') and products_page.has_next() else None,
            'previous': products_page.previous_page_number() if products_page and hasattr(products_page, 'has_previous') and products_page.has_previous() else None,
            'results': [
                {
                    "name": product.name,
                    "slug": product.slug,
                    "image_url": request.build_absolute_uri(product.images.first().image.url)
                    if product.images.first() else None
                }
                for product in products_page
            ]
        }

#Serializer do wyświetlania produktów wraz z kategoriami
class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()  # <-- Zmienione na SerializerMethodField
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'manufacturer', 'images', 'category']

    def get_name(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'name_{lang}', obj.name)

    def get_description(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'description_{lang}', obj.description)

    def get_manufacturer(self, obj):
        if not obj.manufacturer:
            return None

        lang = self.context.get('lang', 'pl')
        name = getattr(obj.manufacturer, f'name_{lang}', obj.manufacturer.name)

        return {
            "id": obj.manufacturer.id,
            "name": name,
            "slug": obj.manufacturer.slug
        }

    def get_category(self, obj):
        categories = obj.categories.all()
        lang = self.context.get('lang', 'pl')

        return [
            {
                "id": category.id,
                "name": getattr(category, f'name_{lang}', category.name),
                "slug": category.slug
            }
            for category in categories
        ]

    def get_images(self, obj):
        images = obj.images.all()
        request = self.context.get('request')

        return [
            {
                "image_url": request.build_absolute_uri(image.image.url) if request else image.image.url
            }
            for image in images
            if image.image
        ]



#############################################################################################################
# Serializery do obsługi API Producenci
#############################################################################################################

#Serializer do liczenia ilości produktów w producencie
class ManufacturerWithProductCountSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'name','slug', 'product_count']

#Serializer do wyświetlania wszystkich producentów
class AllManufacturerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'description']

    def get_name(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'name_{lang}', obj.name)

    def get_description(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'description_{lang}', obj.description)

#Serializer do wyświetlania producentów wraz z produktami
class ManufacturerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['name', 'slug', 'description', 'products']

    def get_name(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.description

    def get_products(self, obj):
        request = self.context.get('request')
        # Domyślne wartości, jeśli request nie jest dostępny
        if not request:
            page_size = 15
            page = 1
        else:
            page_size = int(request.query_params.get('page_size', 15))
            page = int(request.query_params.get('page', 1))

        products = obj.products.all()
        paginator = Paginator(products, page_size)

        try:
            products_page = paginator.page(page)
        except Exception:
            products_page = []

        # Budujemy strukturę paginacji
        return {
            'count': paginator.count,
            'next': products_page.next_page_number() if products_page and products_page.has_next() else None,
            'previous': products_page.previous_page_number() if products_page and products_page.has_previous() else None,
            'results': [
                {
                    "name": product.name,
                    "slug": product.slug,
                    "image_url": request.build_absolute_uri(product.images.first().image.url)
                        if request and product.images.first() else None
                }
                for product in products_page
            ]
        }

#############################################################################################################
# Serializery do obsługi API Kategorie
#############################################################################################################

#Serializer do liczenia ilości produktów w kategorii
class CategoryWithProductCountSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'product_count']

#Serializer do wyświetlania wszystkich kategorii
class AllCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['name', 'slug','description']

    def get_name(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'name_{lang}', obj.name)

    def get_description(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'description_{lang}', obj.description)

#Serializer do wyświetlania kategorii wraz z produktami
class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'description', 'products']

    def get_name(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.description

    def get_products(self, obj):
        request = self.context.get('request')
        page_size = int(request.query_params.get('page_size', 15))
        page = int(request.query_params.get('page', 1))

        # ✅ Obsługa paginacji
        products = obj.products.all()
        paginator = Paginator(products, page_size)

        try:
            products_page = paginator.page(page)
        except:
            products_page = []

        return {
            'count': paginator.count,
            'next': products_page.next_page_number() if products_page.has_next() else None,
            'previous': products_page.previous_page_number() if products_page.has_previous() else None,
            'results': [
                {
                    "name": product.name,
                    "slug": product.slug,
                    "image_url": request.build_absolute_uri(product.images.first().image.url) if product.images.first() else None
                }
                for product in products_page
            ]
        }

#Serializer do wyświetlania kategorii wraz z produktami
class ProductCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description','slug']

    def get_name(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'name_{lang}', obj.name) or obj.name

    def get_description(self, obj):
        lang = self.context.get('lang', 'pl')
        return getattr(obj, f'description_{lang}', obj.description) or obj.description