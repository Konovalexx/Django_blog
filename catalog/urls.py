from django.urls import path
from django.views.decorators.cache import cache_page  # Импортируем cache_page
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductVersionCreateView,
    ProductVersionUpdateView,
)
from django.views.generic import TemplateView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Кэширование данных о продукте на 15 минут (900 секунд)
    path('product/<slug:slug>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),

    path('product/<slug:slug>/version/new/', ProductVersionCreateView.as_view(), name='productversion_create'),
    path('product/<slug:slug>/version/<int:pk>/edit/', ProductVersionUpdateView.as_view(),
         name='productversion_update'),

    path('contacts/', TemplateView.as_view(template_name="catalog/contacts.html"), name='contacts'),
]