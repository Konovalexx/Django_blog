from django.contrib import admin
from catalog.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "category", "is_published", "views_count", "created_at", "price")  # Добавлено 'price'
    search_fields = ("title", "content")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}