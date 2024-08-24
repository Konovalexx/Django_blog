from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductVersionCreateView,
    ProductVersionUpdateView,
    # ProductVersionDeleteView,  # На будущее, для удаления версий
)
from django.views.generic import TemplateView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),  # Создание товара
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Детали товара

    # URL для работы с версиями продуктов
    path('product/<slug:slug>/version/new/', ProductVersionCreateView.as_view(), name='productversion_create'),
    path('product/<slug:slug>/version/<int:pk>/edit/', ProductVersionUpdateView.as_view(),
         name='productversion_update'),
    # path('product/<slug:slug>/version/<int:pk>/delete/', ProductVersionDeleteView.as_view(), name='productversion_delete'),  # Если потребуется
    path('contacts/', TemplateView.as_view(template_name="catalog/contacts.html"), name='contacts'),
]