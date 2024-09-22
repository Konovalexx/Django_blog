from django import forms
from django.utils import timezone
from django.utils.text import slugify
from catalog.models import Article, Newsletter, Blog, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'preview', 'blog', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            # Фильтруем блоги, доступные пользователю
            self.fields['blog'].queryset = Blog.objects.filter(owner=self.user)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]
        if any(word in title.lower() for word in forbidden_words):
            raise forms.ValidationError("Название статьи содержит запрещенные слова.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]
        if any(word in content.lower() for word in forbidden_words):
            raise forms.ValidationError("Содержание статьи содержит запрещенные слова.")
        return content

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            # Автоматическая генерация slug из названия
            title = self.cleaned_data.get('title')
            slug = slugify(title)
            self.cleaned_data['slug'] = slug
        return slug


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'send_at', 'frequency']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'send_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Название рассылки не может быть пустым.")
        return title

    def clean_send_at(self):
        send_at = self.cleaned_data.get('send_at')
        if send_at and send_at < timezone.now():
            raise forms.ValidationError("Дата отправки не может быть в прошлом.")
        return send_at

    def clean_frequency(self):
        frequency = self.cleaned_data.get('frequency')
        if frequency not in ['daily', 'weekly', 'monthly']:
            raise forms.ValidationError("Выберите корректную частоту отправки.")
        return frequency


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
        }
        labels = {
            'content': '',  # Убираем метку поля для более чистого отображения
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Комментарий не может быть пустым.")
        if len(content) < 10:
            raise forms.ValidationError("Комментарий слишком короткий. Минимум 10 символов.")
        forbidden_words = ['казино', 'спам', 'реклама']
        if any(word in content.lower() for word in forbidden_words):
            raise forms.ValidationError("Комментарий содержит запрещенные слова.")
        return content


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Предлагаем название блога по умолчанию, основанное на email пользователя
            if not self.instance.pk:
                self.fields['title'].initial = user.email.split('@')[0]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Название блога не может быть пустым.")
        if Blog.objects.filter(title=title).exists():
            raise forms.ValidationError("Блог с таким названием уже существует.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            description = "Описание по умолчанию для блога."
            self.cleaned_data['description'] = description
        return description