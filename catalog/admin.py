from django.utils.html import format_html
from django.contrib import admin
from catalog.models import Category, Blog, Article, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner")
    search_fields = ("title", "owner__username")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "blog", "created_at", "is_published", "preview_image")
    search_fields = ("title", "content")
    list_filter = ("blog", "is_published")
    prepopulated_fields = {"slug": ("title",)}

    def preview_image(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width: 100px; height: auto;" />', obj.preview.url)
        return "Нет изображения"

    preview_image.short_description = "Превью"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "send_at", "frequency")
    search_fields = ("title", "content")
    list_filter = ("frequency", "owner")