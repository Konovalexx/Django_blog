from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from django.views.generic import TemplateView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),  # Сначала создание товара
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Затем детали товара
    path('contacts/', TemplateView.as_view(template_name="catalog/contacts.html"), name='contacts'),
]