from django.contrib import admin
from catalog.models import Category, Product, ProductVersion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "category", "is_published", "views_count", "created_at", "price")
    search_fields = ("title", "content")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "version_number", "version_name", "is_current")
    search_fields = ("version_number", "version_name")
    list_filter = ("product", "is_current")
    ordering = ("-is_current", "product", "version_number")