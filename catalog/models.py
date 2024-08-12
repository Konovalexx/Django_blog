from django.db import models
from django.utils import timezone
from django.db import models, connection


class Category(models.Model):
    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')


    name = models.CharField(
        max_length=150,
        verbose_name="Категория",
        help_text="Введите название категории:",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории:",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')


    name = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите название товара: ",
    )
    description = models.TextField(verbose_name="Описание", help_text="Опишите товар: ")
    image = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото товара:",
    )
    price = models.IntegerField(blank=True, null=True, verbose_name="Цена за покупку")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите название категории",
        blank=True,
        null=True,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "price"]

    def __str__(self):
        return self.name
