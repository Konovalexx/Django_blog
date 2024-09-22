from django.db import models
from django.utils.text import slugify
from django.db import connection
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils import timezone

class Category(models.Model):
    """Модель для категорий блогов."""
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


class Blog(models.Model):
    """Модель для блогов, которые могут быть созданы пользователями."""
    title = models.CharField(
        max_length=255,
        verbose_name="Название блога",
        help_text="Введите название блога:",
    )
    description = models.TextField(
        verbose_name="Описание блога",
        help_text="Введите описание блога:",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name="Владелец блога",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True,
        blank=True,
        related_name="blogs",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title


class ArticleManager(models.Manager):
    def published(self):
        """Возвращает только опубликованные статьи."""
        return self.filter(is_published=True)

    def drafts(self):
        """Возвращает только черновики."""
        return self.filter(is_published=False)


class Article(models.Model):
    """Модель для статей, которые привязаны к конкретным блогам."""
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи:",
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-метка",
        help_text="Введите URL-метку статьи:",
        null=True,
    )
    content = models.TextField(
        default='',
        verbose_name="Содержимое",
        help_text="Введите содержание статьи:",
    )
    preview = models.ImageField(
        upload_to="catalog/previews",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение превью статьи:",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    blog = models.ForeignKey(
        Blog,
        on_delete=models.SET_NULL,
        verbose_name="Блог",
        help_text="Выберите блог, к которому относится статья:",
        blank=True,
        null=True,
        related_name="articles",
    )

    objects = ArticleManager()  # Подключаем кастомный менеджер

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def can_moderate(self, user):
        """Проверка прав на модерирование статьи."""
        if user.has_perm('catalog.change_article') or self.blog.owner == user:
            return True
        raise PermissionDenied("У вас нет прав на изменение этой статьи.")


class Newsletter(models.Model):
    """Модель для рассылок, которые могут создавать пользователи."""
    title = models.CharField(
        max_length=255,
        verbose_name="Название рассылки",
    )
    content = models.TextField(
        verbose_name="Содержимое рассылки",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='newsletters',
        verbose_name="Владелец рассылки",
    )
    send_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата отправки")
    frequency = models.CharField(
        max_length=50,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        verbose_name="Частота отправки",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.title

    def is_scheduled(self):
        """Проверка, запланирована ли рассылка."""
        return self.send_at and self.send_at > timezone.now()


class Comment(models.Model):
    """Модель для комментариев к статьям."""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Статья",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария",
    )
    content = models.TextField(
        verbose_name="Комментарий",
        help_text="Введите ваш комментарий:",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_moderated = models.BooleanField(default=False, verbose_name="Проверено модератором")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.author} к статье {self.article.title}"

    def can_moderate(self, user):
        """Проверка прав модератора на комментарий."""
        if user.has_perm('catalog.change_comment'):
            return True
        raise PermissionDenied("У вас нет прав на изменение этого комментария.")