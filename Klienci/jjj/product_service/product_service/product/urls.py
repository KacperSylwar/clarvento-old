from django.urls import path
from .views import (
    ProductDetailViewBySlug,
ProductListView,
CategoryListView,
CategoryWithProductCountView,
ManufacturerWithProductCountView,
CategoryDetailView,
ProductHomepageView,
ManufacturerListView,
ManufacturerDetailView,
CSVUploadView

)

urlpatterns = [
    path('<str:lang>/products/',ProductListView.as_view(), name='products'),
    path('<str:lang>/product/<slug:slug>/', ProductDetailViewBySlug.as_view(), name='product-detail-by-slug'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('categories-with-count/', CategoryWithProductCountView.as_view(), name='categories-with-count'),
    path('manufacturers-with-count/', ManufacturerWithProductCountView.as_view(), name='manufacturers-with-count'),
    path('homepage/', ProductHomepageView.as_view(), name='homepage'),
    path('manufacturers/', ManufacturerListView.as_view(), name='manufacturers'),
    path('manufacturer/<slug:slug>/', ManufacturerDetailView.as_view(), name='manufacturer'),
]

