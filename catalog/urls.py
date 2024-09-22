from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import LogoutView, LoginView  # Добавленный импорт
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    NewsletterCreateView,
    NewsletterUpdateView,
    BlogCreateView,
)
from django.views.generic import TemplateView

app_name = 'catalog'

urlpatterns = [
    # Список статей
    path('', ArticleListView.as_view(), name='article_list'),

    # Создание новой статьи
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),

    # Редактирование статьи
    path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),

    # Удаление статьи
    path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # Детали статьи с кэшированием на 15 минут
    path('article/<slug:slug>/', cache_page(60 * 15)(ArticleDetailView.as_view()), name='article_detail'),

    # Создание новой рассылки
    path('newsletter/new/', NewsletterCreateView.as_view(), name='newsletter_create'),

    # Редактирование рассылки
    path('newsletter/<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletter_update'),

    # Создание блога
    path('blog/new/', BlogCreateView.as_view(), name='blog_create'),

    # Контакты
    path('contacts/', TemplateView.as_view(template_name="catalog/contacts.html"), name='contacts'),

    # Вход в аккаунт
    path('login/', LoginView.as_view(), name='login'),  # Добавленный маршрут

    # Выход из аккаунта
    path('logout/', LogoutView.as_view(), name='logout'),
]