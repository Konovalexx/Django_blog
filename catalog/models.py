from django.db import models
from django.utils.text import slugify
from django.db import connection

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

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок товара:",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-метка",
        help_text="Введите URL-метку товара:",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите описание товара:",
    )
    preview = models.ImageField(
        upload_to="catalog/previews",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение превью товара:",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию товара:",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.IntegerField(
        default=0,  # Значение по умолчанию
        verbose_name="Цена",
        help_text="Введите цену товара:",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title