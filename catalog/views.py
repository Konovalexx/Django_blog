from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from catalog.models import Article, Newsletter, Blog, Comment
from catalog.forms import ArticleForm, NewsletterForm, CommentForm, BlogForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# Список статей
class ArticleListView(ListView):
    model = Article
    template_name = 'catalog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        filter_option = self.request.GET.get('filter', 'all')
        blog_id = self.request.GET.get('blog_id')
        search_query = self.request.GET.get('search', '')

        if user.is_authenticated and filter_option == 'all':
            filter_option = 'forum'

        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists():
                articles = Article.objects.all()
            else:
                articles = Article.objects.filter(blog__owner=user)

                if filter_option == 'published':
                    articles = articles.filter(is_published=True)
                elif filter_option == 'drafts':
                    articles = articles.filter(is_published=False)
                elif filter_option == 'forum':
                    articles = Article.objects.filter(is_published=True)
        else:
            articles = Article.objects.filter(is_published=True)

        if blog_id:
            articles = articles.filter(blog__id=blog_id)

        if search_query:
            articles = articles.filter(title__icontains=search_query)

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'forum')
        context['blogs'] = Blog.objects.filter(owner=self.request.user) if self.request.user.is_authenticated else []
        context['search'] = self.request.GET.get('search', '')
        return context


# Просмотр статьи
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'catalog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_moderator'] = user.groups.filter(name='Moderators').exists()
        context['comment_form'] = CommentForm() if user.is_authenticated else None
        context['comments'] = Comment.objects.filter(article=self.get_object())
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        article = self.get_object()
        if article.is_published:
            article.views_count += 1
            article.save()
        return response


# Создание статьи
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:article_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.author = self.request.user.email.split('@')[0].capitalize()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(owner=self.request.user)
        return context


# Редактирование статьи
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'catalog/article_form.html'
    success_url = reverse_lazy('catalog:article_list')

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.blog.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете редактировать эту статью.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user.email.split('@')[0].capitalize()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(owner=self.request.user)
        return context


# Удаление статьи
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'catalog/article_confirm_delete.html'
    success_url = reverse_lazy('catalog:article_list')

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.blog.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете удалить эту статью.")
        return super().dispatch(request, *args, **kwargs)


# Создание комментария
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'catalog/article_detail.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = get_object_or_404(Article, id=self.kwargs['article_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:article_detail', kwargs={'pk': self.kwargs['article_id']})


# Управление рассылками
class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'catalog/newsletter_form.html'
    success_url = reverse_lazy('catalog:article_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'catalog/newsletter_form.html'
    success_url = reverse_lazy('catalog:article_list')

    def dispatch(self, request, *args, **kwargs):
        newsletter = self.get_object()
        if newsletter.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете обновлять эту рассылку.")
        return super().dispatch(request, *args, **kwargs)


# Управление блогами
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'catalog/blog_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:article_create')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'catalog/blog_form.html'

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете редактировать этот блог.")
        return super().dispatch(request, *args, **kwargs)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'catalog/blog_confirm_delete.html'
    success_url = reverse_lazy('catalog:article_list')

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете удалить этот блог.")
        return super().dispatch(request, *args, **kwargs)