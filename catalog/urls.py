from django.urls import path
from catalog.apps import CatalogConfig
from .views import (
    HomeView, ContactsView, ProductListView,
    ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    publish_product, unpublish_product,
    category_products
)

app_name = CatalogConfig.name

urlpatterns = [
    # Основные страницы
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # CRUD для продуктов
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # ПУТИ ДЛЯ ПУБЛИКАЦИИ И СНЯТИЯ С ПУБЛИКАЦИИ
    path('product/<int:pk>/publish/', publish_product, name='publish_product'),
    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),

    # НОВЫЙ ПУТЬ ДЛЯ ПРОДУКТОВ ПО КАТЕГОРИИ
    path('category/<slug:category_slug>/', category_products, name='category_products'),
]