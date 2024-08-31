# Generated by Django 5.0.7 on 2024-08-28 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название категории:",
                        max_length=150,
                        verbose_name="Категория",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание категории:",
                        null=True,
                        verbose_name="Описание категории",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="ProductVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version_number",
                    models.CharField(max_length=50, verbose_name="Номер версии"),
                ),
                (
                    "version_name",
                    models.CharField(max_length=255, verbose_name="Название версии"),
                ),
                (
                    "is_current",
                    models.BooleanField(default=False, verbose_name="Текущая версия"),
                ),
            ],
            options={
                "verbose_name": "Версия продукта",
                "verbose_name_plural": "Версии продуктов",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="Введите заголовок товара:",
                        max_length=255,
                        null=True,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Введите URL-метку товара:",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="URL-метка",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        default="",
                        help_text="Введите описание товара:",
                        verbose_name="Содержимое",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение превью товара:",
                        null=True,
                        upload_to="catalog/previews",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Признак публикации"
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
                (
                    "price",
                    models.IntegerField(
                        default=0, help_text="Введите цену товара:", verbose_name="Цена"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        help_text="Выберите категорию товара:",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="catalog.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
        ),
    ]
