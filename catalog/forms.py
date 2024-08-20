from django import forms
from catalog.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'content', 'preview', 'category', 'is_published', 'price']  # Добавлено 'price'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }